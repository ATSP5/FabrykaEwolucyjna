import os

import pandas as pd

from MachineGroup import MachineGroup
from ProductionOrder import ProductionOrder
from Recipe import Recipe


class AnalysisFileWriter:
    """Keeps the data of the analysis as tables and writes them, with the best schedule, to CSV."""

    def __init__(self, machines: list[MachineGroup], recipes: list[Recipe], orders: list[ProductionOrder],
                 report: dict, folder: str = ""):
        self.machines = machines
        self.recipes = recipes
        self.orders = orders
        self.report = report
        self.folder = folder or os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    def input_tables(self) -> dict[str, pd.DataFrame]:
        machines = pd.DataFrame([{"Maszyna": group.name, "Sztuk": group.count} for group in self.machines])
        recipes = pd.DataFrame([{
            "Produkt": recipe.product,
            "Przepis": " → ".join("%s %d min" % (step.machine, step.minutes) for step in recipe.steps),
            "Razem [min]": recipe.total_minutes,
        } for recipe in self.recipes])
        orders = pd.DataFrame([{
            "Zlecenie": order.order_id, "Produkt": order.product, "Priorytet": order.weight,
            "Napływ [min]": order.arrival_minute, "Deadline [min]": order.deadline_minutes,
            "Termin [min]": order.due_minute,
        } for order in self.orders])
        return {"machines": machines, "recipes": recipes, "orders": orders}

    def written_paths(self) -> list[str]:
        os.makedirs(self.folder, exist_ok=True)
        tables = self.input_tables()
        evolution_name = self.report["evolution_name"]
        tables["best_schedule"] = self.report["operations"][evolution_name]
        tables["order_outcomes"] = self.report["outcomes"][evolution_name]
        paths = []
        for name, table in tables.items():
            path = os.path.join(self.folder, name + ".csv")
            table.to_csv(path, index=False, encoding="utf-8-sig")
            paths.append(path)
        return paths
