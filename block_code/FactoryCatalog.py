from MachineGroup import MachineGroup
from Recipe import Recipe
from RecipeStep import RecipeStep


class FactoryCatalog:
    """The factory's fixed data: its machines and the recipe of every product."""

    MACHINES = (("A", 3), ("B", 4), ("C", 2), ("D", 1), ("E", 5), ("F", 8))
    RECIPES = {
        "X": (("A", 30), ("B", 10), ("A", 4), ("D", 8), ("C", 8), ("E", 12), ("F", 15), ("B", 8), ("E", 8), ("F", 12)),
        "Y": (("B", 10), ("C", 8), ("E", 10), ("F", 10), ("A", 5), ("E", 9), ("D", 3), ("F", 13), ("B", 9), ("C", 5), ("E", 6), ("F", 9)),
        "Z": (("A", 6), ("C", 9), ("F", 12), ("E", 8), ("B", 8), ("F", 8), ("D", 2), ("A", 5), ("E", 7), ("C", 4), ("F", 14), ("B", 6), ("E", 5), ("F", 7)),
        "V": (("F", 17), ("E", 14), ("B", 11), ("F", 14), ("A", 7), ("E", 11), ("C", 7), ("F", 11), ("D", 4)),
        "W": (("C", 8), ("D", 3), ("F", 13), ("A", 8), ("B", 9), ("E", 9), ("F", 10), ("C", 5), ("A", 6), ("E", 8), ("B", 8), ("F", 9), ("D", 2)),
        "Q": (("E", 6), ("F", 8), ("B", 6), ("F", 6), ("A", 4), ("E", 7), ("C", 4), ("F", 9), ("B", 5), ("E", 5), ("D", 2), ("F", 7), ("A", 3), ("E", 6), ("B", 6), ("F", 6)),
        "R": (("B", 11), ("A", 9), ("C", 8), ("E", 10), ("D", 4), ("F", 11), ("B", 10), ("A", 6), ("E", 9), ("F", 9), ("C", 4)),
        "S": (("F", 15), ("E", 13), ("B", 12), ("A", 7), ("F", 13), ("D", 3), ("E", 12), ("F", 12)),
    }

    def machines(self) -> list[MachineGroup]:
        return [MachineGroup(name, count) for name, count in self.MACHINES]

    def recipes(self) -> list[Recipe]:
        return [Recipe(product, tuple(RecipeStep(machine, minutes) for machine, minutes in steps))
                for product, steps in self.RECIPES.items()]
