import numpy as np

from EvolutionResult import EvolutionResult
from FactoryProblem import FactoryProblem
from ScheduledOperation import ScheduledOperation


class ScheduleDecoder:
    """Turns chromosomes back into full schedules, independently of the GPU's decoder."""

    EVOLUTION_NAME = "Algorytm ewolucyjny"

    def __init__(self, problem: FactoryProblem, result: EvolutionResult, seeds: dict[str, np.ndarray]):
        self.problem = problem
        self.result = result
        self.seeds = seeds

    def schedules(self) -> dict[str, list[ScheduledOperation]]:
        decoded = {self.EVOLUTION_NAME: self._decode(self.result.best_chromosome)}
        for rule, chromosome in self.seeds.items():
            decoded[rule] = self._decode(chromosome)
        return decoded

    def _decode(self, chromosome: np.ndarray) -> list[ScheduledOperation]:
        problem = self.problem
        offsets = problem.job_op_offset.tolist()
        next_op = offsets[:-1]
        ready = problem.job_arrival.tolist()
        machine_free = [0] * problem.machines
        operations = []
        for job in chromosome.tolist():
            op = next_op[job]
            next_op[job] = op + 1
            machine, start = problem.pick_machine(machine_free, int(problem.op_machine_type[op]), ready[job])
            end = start + int(problem.op_minutes[op])
            machine_free[machine] = end
            ready[job] = end
            operations.append(ScheduledOperation(job, op - offsets[job], machine, start, end))
        return operations
