from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FactoryProblem:
    """The scheduling problem as flat int32 arrays, the shape the CUDA kernels read."""

    machine_types: tuple[str, ...]
    machine_labels: tuple[str, ...]
    order_ids: tuple[str, ...]
    products: tuple[str, ...]
    job_op_offset: np.ndarray
    op_machine_type: np.ndarray
    op_minutes: np.ndarray
    job_arrival: np.ndarray
    job_due: np.ndarray
    job_weight: np.ndarray
    type_machine_offset: np.ndarray
    tardiness_scale: int

    @property
    def jobs(self) -> int:
        return len(self.order_ids)

    @property
    def genes(self) -> int:
        return int(self.op_minutes.size)

    @property
    def machines(self) -> int:
        return len(self.machine_labels)

    def base_chromosome(self) -> np.ndarray:
        """Every job number repeated once per recipe step, the genes every individual permutes."""
        return np.repeat(np.arange(self.jobs, dtype=np.int32), np.diff(self.job_op_offset))

    def pick_machine(self, machine_free: list[int], machine_type: int, ready: int) -> tuple[int, int]:
        """The same rule as the EvaluateSchedules kernel: (machine, start minute)."""
        first = int(self.type_machine_offset[machine_type])
        last = int(self.type_machine_offset[machine_type + 1])
        best_machine, best_start, best_free = first, 2147483647, -1
        for machine in range(first, last):
            free_at = machine_free[machine]
            start = max(free_at, ready)
            if start < best_start or (start == best_start and free_at > best_free):
                best_machine, best_start, best_free = machine, start, free_at
        return best_machine, best_start
