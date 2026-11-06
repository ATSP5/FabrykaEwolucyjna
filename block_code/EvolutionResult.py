from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class EvolutionResult:
    """What the evolution on the GPU found, and how it got there."""

    best_chromosome: np.ndarray
    best_cost: int
    history: pd.DataFrame
    individuals: int
    generations: int
    seconds: float
    device: str
