from dataclasses import dataclass


@dataclass(frozen=True)
class RecipeStep:
    """One step of a recipe: the machine type it needs and how long it takes."""

    machine: str
    minutes: int
