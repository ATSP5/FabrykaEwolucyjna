import numpy as np

from FactoryProblem import FactoryProblem


class PopulationInitializer:
    """Builds generation zero on the grid and the parameter vector the kernels read."""

    def __init__(self, problem: FactoryProblem, seeds: dict[str, np.ndarray], grid_side: int = 64,
                 random_seed: int = 7, seeded_share: float = 0.5, arrival_noise_minutes: float = 60.0,
                 neighbourhood_radius: int = 2, crossover_permille: int = 900, mutation_permille: int = 600,
                 mutation_max_swaps: int = 4, mutation_window: int = 30):
        if not 4 <= grid_side <= 512:
            raise ValueError("grid_side must be between 4 and 512")
        if not 0.0 <= seeded_share <= 1.0:
            raise ValueError("seeded_share must be between 0 and 1")
        if arrival_noise_minutes < 0.0:
            raise ValueError("arrival_noise_minutes must not be negative")
        if not 1 <= neighbourhood_radius <= grid_side // 2:
            raise ValueError("neighbourhood_radius must be between 1 and grid_side / 2")
        if not 0 <= crossover_permille <= 1000 or not 0 <= mutation_permille <= 1000:
            raise ValueError("crossover_permille and mutation_permille must be between 0 and 1000")
        if mutation_max_swaps < 1 or mutation_window < 1:
            raise ValueError("mutation_max_swaps and mutation_window must be at least 1")
        self.problem = problem
        self.seed_chromosomes = list(seeds.values())
        self.grid_side = grid_side
        self.random_seed = random_seed
        self.seeded_share = seeded_share
        self.arrival_noise_minutes = arrival_noise_minutes
        self.neighbourhood_radius = neighbourhood_radius
        self.crossover_permille = crossover_permille
        self.mutation_permille = mutation_permille
        self.mutation_max_swaps = mutation_max_swaps
        self.mutation_window = mutation_window

    def population(self) -> np.ndarray:
        """individuals x genes int32 values, one row per grid cell, as one contiguous array."""
        rng = np.random.default_rng(self.random_seed)
        problem = self.problem
        individuals = self.grid_side * self.grid_side
        cells = np.empty((individuals, problem.genes), dtype=np.int32)
        for cell in range(individuals):
            if rng.random() < self.seeded_share:
                cells[cell] = self._perturbed_seed(rng)
            else:
                cells[cell] = self._arrival_biased(rng)
        # The rules themselves, unchanged and spread over the grid: the evolution cannot end worse.
        for number, seed in enumerate(self.seed_chromosomes):
            cells[(2 * number + 1) * individuals // (2 * len(self.seed_chromosomes))] = seed
        return cells.ravel()

    def _perturbed_seed(self, rng: np.random.Generator) -> np.ndarray:
        chromosome = self.seed_chromosomes[int(rng.integers(len(self.seed_chromosomes)))].copy()
        genes = chromosome.size
        for _ in range(int(rng.integers(1, 2 * self.mutation_max_swaps + 1))):
            left = int(rng.integers(genes))
            right = min(left + 1 + int(rng.integers(self.mutation_window)), genes - 1)
            chromosome[left], chromosome[right] = chromosome[right], chromosome[left]
        return chromosome

    def _arrival_biased(self, rng: np.random.Generator) -> np.ndarray:
        base = self.problem.base_chromosome()
        keys = self.problem.job_arrival[base] + rng.normal(0.0, self.arrival_noise_minutes, base.size)
        return base[np.argsort(keys)]

    def params(self) -> np.ndarray:
        problem = self.problem
        return np.array([
            self.grid_side * self.grid_side,  # 0 individuals
            problem.genes,                    # 1 genes
            problem.jobs,                     # 2 jobs
            problem.machines,                 # 3 machines
            self.grid_side,                   # 4 grid side
            0,                                # 5 generation, set by EvolutionEngine before each step
            self.random_seed,                 # 6 seed
            self.neighbourhood_radius,        # 7 neighbourhood radius
            self.mutation_permille,           # 8 mutation chance per mille
            self.mutation_max_swaps,          # 9 most swaps per child
            self.mutation_window,             # 10 swap window
            problem.tardiness_scale,          # 11 tardiness scale
            self.crossover_permille,          # 12 crossover chance per mille
        ], dtype=np.int32)
