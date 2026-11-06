Przepis na obraz Dockera do uruchomień na GPU: CUDA 12.2, Python 3.10 i PyCUDA. Jest osobnym blokiem, bo Run Engine nie doinstalowuje pakietów `apt`, a PyCUDA nie ma koła dla Linuksa i kompiluje się dopiero z `python3-dev`. Blok nie jest wykonywany ani połączony; *Generate Source* zapisuje go jako `Dockerfile`, a używa go blok *Docker Compose (GPU run image)*.

## FROM
Obraz bazowy `nvidia/cuda:12.2.2-devel-ubuntu22.04`. CUDA 12.2 obsługuje Pascala (`sm_61`) i nie jest nowsza od CUDA 12.8 ze sterownika 571.96. Wersja 13.x nie obsługuje tej karty.

## ENV
Zmienne budowania bez wpływu na wyniki analizy: tryb nieinteraktywny `apt` oraz `pip` bez pamięci podręcznej, co zmniejsza obraz.

## RUN apt-get
Instaluje `python3`, `python3-pip`, `python3-dev` i `python-is-python3`. Bez `python3-dev` budowanie PyCUDA kończy się błędem `Failed building wheel for pycuda`.

## RUN pip install
Przypina `numpy==2.2.6`, `pandas==2.3.3` i `pycuda==2026.1`, te same wersje co na liście Manual w Run Engine. Inne wersje mogą zmienić zachowanie i muszą być zmienione w obu miejscach.

## WORKDIR
Katalog `/app`, do którego CatNip montuje projekt. Tam leżą `main_1.py` i pliki `.ptx`.
