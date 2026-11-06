import os
import sys
if sys.platform == 'win32':
    import os as _os
    _cuda_done = False
    _roots = [_os.environ.get('CUDA_PATH', '')] + [rf'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v{_v}' for _v in ['12.8', '12.6', '12.5', '12.4', '12.3', '12.2', '12.1', '12.0', '11.8']]
    for _root in [r for r in _roots if r]:
        for _sub in [r'bin\x64', 'bin']:
            _p = _os.path.join(_root, _sub)
            if _os.path.isdir(_p) and any(f.endswith('.dll') for f in _os.listdir(_p)):
                _os.add_dll_directory(_p)
                _cuda_done = True
                break
        if _cuda_done: break
import pycuda.driver as drv
import pycuda.autoinit


class CUDAKernelLoader:
    """Opens the three kernels of the evolution, one method per kernel returning its handle."""

    def __init__(self, ptx_dir: str = ""):
        self.ptx_dir = ptx_dir
        self._evaluate = self._load("EvaluateSchedules")
        self._breed = self._load("BreedGeneration")
        self._replace = self._load("ReplaceSurvivors")

    def _search_dirs(self) -> list:
        here = os.path.dirname(os.path.abspath(__file__))
        return [d for d in (self.ptx_dir, os.getcwd(), here, os.path.dirname(here)) if d]

    def _find(self, names: tuple) -> str:
        for directory in self._search_dirs():
            for name in names:
                path = os.path.join(directory, name)
                if os.path.isfile(path):
                    return path
        return None

    def _load(self, kernel_name: str):
        ptx_path = self._find((kernel_name.lower() + ".ptx", kernel_name + ".ptx"))
        if ptx_path:
            with open(ptx_path, "rb") as ptx_file:
                module = drv.module_from_buffer(ptx_file.read())
            print("[CUDA] %s: %s" % (kernel_name, ptx_path))
            return module
        return self._compile_source(kernel_name)

    def _compile_source(self, kernel_name: str):
        from pycuda.compiler import SourceModule
        source_path = self._find((kernel_name + ".cu", os.path.join("block_code", kernel_name + ".cu")))
        if source_path is None:
            raise FileNotFoundError("No PTX and no source for %s in %s: run Compile CUDA Kernels first"
                                    % (kernel_name, self._search_dirs()))
        with open(source_path, encoding="utf-8") as source_file:
            module = SourceModule(source_file.read(), no_extern_c=True)
        print("[CUDA] %s: %s (compiled by nvcc at run time)" % (kernel_name, source_path))
        return module

    def evaluate_schedules(self):
        return self._evaluate.get_function("kernel")

    def breed_generation(self):
        return self._breed.get_function("kernel")

    def replace_survivors(self):
        return self._replace.get_function("kernel")
