import math

import numpy as np

from MachineGroup import MachineGroup
from ProductionOrder import ProductionOrder
from Recipe import Recipe


class OrderStreamGenerator:
    """A random, reproducible stream of orders, sized to load the factory's busiest machine type."""

    def __init__(self, machines: list[MachineGroup], recipes: list[Recipe], seed: int = 2026,
                 shift_minutes: int = 480, bottleneck_load: float = 0.9,
                 deadline_minutes: tuple = (60, 90, 120, 180, 240), weights: tuple = (1, 1, 1, 2, 3),
                 min_slack_ratio: float = 1.2):
        if shift_minutes <= 0:
            raise ValueError("shift_minutes must be positive")
        if not 0.0 < bottleneck_load <= 1.5:
            raise ValueError("bottleneck_load must be in (0, 1.5]")
        if not deadline_minutes or min(deadline_minutes) <= 0:
            raise ValueError("deadline_minutes must hold positive values")
        if not weights or min(weights) <= 0:
            raise ValueError("weights must hold positive values")
        if min_slack_ratio < 1.0:
            raise ValueError("min_slack_ratio must be at least 1")
        self.machines = machines
        self.recipes = recipes
        self.seed = seed
        self.shift_minutes = shift_minutes
        self.bottleneck_load = bottleneck_load
        self.deadline_minutes = sorted(deadline_minutes)
        self.weights = weights
        self.min_slack_ratio = min_slack_ratio

    def _orders_per_minute(self) -> float:
        counts = {group.name: group.count for group in self.machines}
        demand = {name: 0.0 for name in counts}
        for recipe in self.recipes:
            for step in recipe.steps:
                demand[step.machine] += step.minutes / len(self.recipes)
        minutes_per_order_on_busiest = max(demand[name] / counts[name] for name in counts)
        return self.bottleneck_load / minutes_per_order_on_busiest

    def _deadline_for(self, recipe: Recipe, rng: np.random.Generator) -> int:
        shortest = recipe.total_minutes * self.min_slack_ratio
        allowed = [minutes for minutes in self.deadline_minutes if minutes >= shortest]
        if not allowed:
            return int(math.ceil(shortest / 30.0) * 30)
        return int(rng.choice(allowed))

    def orders(self) -> list[ProductionOrder]:
        rng = np.random.default_rng(self.seed)
        mean_gap = 1.0 / self._orders_per_minute()
        stream = []
        clock = float(rng.exponential(mean_gap))
        while clock < self.shift_minutes:
            recipe = self.recipes[int(rng.integers(len(self.recipes)))]
            stream.append(ProductionOrder(order_id="Z%04d" % (len(stream) + 1), product=recipe.product,
                                          arrival_minute=int(clock),
                                          deadline_minutes=self._deadline_for(recipe, rng),
                                          weight=int(rng.choice(self.weights))))
            clock += float(rng.exponential(mean_gap))
        return stream
