import time

import numpy as np
import pandas as pd
import pycuda.driver as drv

from EvolutionResult import EvolutionResult
from FactoryProblem import FactoryProblem
from PolishNumberFormat import PolishNumberFormat


class EvolutionEngine:
    """Runs the generations: holds the buffers on the GPU and launches the kernels in order."""

    GENERATION_SLOT = 5

    def __init__(self, evaluate_schedules, breed_generation, replace_survivors, problem: FactoryProblem,
                 population: np.ndarray, params: np.ndarray, formatter: PolishNumberFormat,
                 generations: int = 3000, log_every: int = 25, block_size: int = 256):
        if generations < 1:
            raise ValueError("generations must be at least 1")
        if log_every < 1:
            raise ValueError("log_every must be at least 1")
        if not 32 <= block_size <= 1024:
            raise ValueError("block_size must be between 32 and 1024")
        self.evaluate_schedules = evaluate_schedules
        self.breed_generation = breed_generation
        self.replace_survivors = replace_survivors
        self.problem = problem
        self.population = np.ascontiguousarray(population, dtype=np.int32)
        self.params = np.array(params, dtype=np.int32)
        self.formatter = formatter
        self.generations = generations
        self.log_every = log_every
        self.block_size = block_size
        self.individuals = int(self.params[0])
        self.grid = ((self.individuals + block_size - 1) // block_size, 1)

    def result(self) -> EvolutionResult:
        started = time.perf_counter()
        problem_buffers = [drv.to_device(array) for array in (
            self.problem.job_op_offset, self.problem.op_machine_type, self.problem.op_minutes,
            self.problem.job_arrival, self.problem.job_due, self.problem.job_weight,
            self.problem.type_machine_offset)]
        size = np.int32(self.population.size)
        block = (self.block_size, 1, 1)
        params = drv.to_device(self.params)
        population = drv.to_device(self.population)
        next_population = drv.mem_alloc(self.population.nbytes)
        children = drv.mem_alloc(self.population.nbytes)
        cost = drv.mem_alloc(self.individuals * 4)
        next_cost = drv.mem_alloc(self.individuals * 4)
        children_cost = drv.mem_alloc(self.individuals * 4)
        step_params = self.params.copy()

        self.evaluate_schedules(population, *problem_buffers, params, size, cost, block=block, grid=self.grid)
        history = [self._record(0, cost)]
        for generation in range(1, self.generations + 1):
            step_params[self.GENERATION_SLOT] = generation
            drv.memcpy_htod(params, step_params)
            self.breed_generation(population, cost, params, size, children, block=block, grid=self.grid)
            self.evaluate_schedules(children, *problem_buffers, params, size, children_cost, block=block, grid=self.grid)
            self.replace_survivors(population, cost, children, children_cost, params, size,
                                   next_population, next_cost, block=block, grid=self.grid)
            population, next_population = next_population, population
            cost, next_cost = next_cost, cost
            if generation % self.log_every == 0 or generation == self.generations:
                history.append(self._record(generation, cost))
                if generation * 10 // self.generations != (generation - self.log_every) * 10 // self.generations:
                    self._print_progress(history[-1])

        costs = np.empty(self.individuals, dtype=np.int32)
        drv.memcpy_dtoh(costs, cost)
        best_cell = int(np.argmin(costs))
        final = np.empty(self.population.size, dtype=np.int32)
        drv.memcpy_dtoh(final, population)
        genes = self.problem.genes
        return EvolutionResult(best_chromosome=final[best_cell * genes:(best_cell + 1) * genes].copy(),
                               best_cost=int(costs[best_cell]), history=pd.DataFrame(history),
                               individuals=self.individuals, generations=self.generations,
                               seconds=time.perf_counter() - started, device=drv.Context.get_device().name())

    def _record(self, generation: int, cost) -> dict:
        costs = np.empty(self.individuals, dtype=np.int32)
        drv.memcpy_dtoh(costs, cost)
        return {"Pokolenie": generation, "Najlepszy koszt": int(costs.min()), "Średni koszt": float(costs.mean())}

    def _print_progress(self, row: dict) -> None:
        number = self.formatter.number
        print("[GPU] pokolenie %s z %s: najlepszy koszt %s, średni %s" % (
            number(row["Pokolenie"], 0), number(self.generations, 0),
            number(row["Najlepszy koszt"], 0), number(row["Średni koszt"], 0)))
