from dataclasses import dataclass

from RecipeStep import RecipeStep


@dataclass(frozen=True)
class Recipe:
    """The ordered steps that make one product."""

    product: str
    steps: tuple[RecipeStep, ...]

    @property
    def total_minutes(self) -> int:
        return sum(step.minutes for step in self.steps)
