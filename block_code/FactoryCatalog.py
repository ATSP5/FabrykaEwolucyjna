from MachineGroup import MachineGroup
from Recipe import Recipe
from RecipeStep import RecipeStep


class FactoryCatalog:
    """The factory's fixed data: its machines and the recipe of every product."""

    MACHINES = (("A", 3), ("B", 4), ("C", 2), ("D", 1), ("E", 5), ("F", 8))
    RECIPES = {
        "X": (("A", 30), ("B", 10), ("A", 4), ("D", 8)),
        "Y": (("B", 12), ("C", 15), ("E", 10)),
        "Z": (("A", 8), ("C", 20), ("F", 15), ("E", 6)),
        "V": (("F", 25), ("E", 20), ("B", 5)),
        "W": (("C", 10), ("D", 6), ("F", 20), ("A", 12)),
        "Q": (("E", 15), ("F", 30), ("F", 10), ("B", 8)),
        "R": (("B", 20), ("A", 15), ("C", 12), ("E", 8), ("D", 5)),
        "S": (("F", 12), ("E", 12)),
    }

    def machines(self) -> list[MachineGroup]:
        return [MachineGroup(name, count) for name, count in self.MACHINES]

    def recipes(self) -> list[Recipe]:
        return [Recipe(product, tuple(RecipeStep(machine, minutes) for machine, minutes in steps))
                for product, steps in self.RECIPES.items()]
