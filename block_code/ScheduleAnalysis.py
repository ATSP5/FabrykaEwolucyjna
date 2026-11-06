import pandas as pd

from EvolutionResult import EvolutionResult
from FactoryProblem import FactoryProblem
from ScheduledOperation import ScheduledOperation


class ScheduleAnalysis:
    """Checks every schedule, then measures it: lateness, makespan and machine use."""

    def __init__(self, problem: FactoryProblem, result: EvolutionResult, schedules: dict[str, list[ScheduledOperation]],
                 evolution_name: str = "Algorytm ewolucyjny"):
        self.problem = problem
        self.result = result
        self.all_schedules = schedules
        self.evolution_name = evolution_name
        for name, operations in schedules.items():
            self._verify(name, operations)
        verified = self._cost(schedules[evolution_name])
        if verified != result.best_cost:
            raise RuntimeError("GPU cost %d differs from the Python decoder's %d" % (result.best_cost, verified))

    def _verify(self, name: str, operations: list[ScheduledOperation]) -> None:
        problem = self.problem
        if len(operations) != problem.genes:
            raise RuntimeError("%s: %d operations, expected %d" % (name, len(operations), problem.genes))
        machine_end = {}
        for operation in sorted(operations, key=lambda item: item.start_minute):
            if operation.start_minute < machine_end.get(operation.machine, 0):
                raise RuntimeError("%s: machine %s runs two operations at once" % (name, problem.machine_labels[operation.machine]))
            machine_end[operation.machine] = operation.end_minute
        job_end = problem.job_arrival.tolist()
        for operation in sorted(operations, key=lambda item: (item.job, item.step)):
            if operation.start_minute < job_end[operation.job]:
                raise RuntimeError("%s: %s starts a step before it may" % (name, problem.order_ids[operation.job]))
            job_end[operation.job] = operation.end_minute

    def _finish_minutes(self, operations: list[ScheduledOperation]) -> list[int]:
        finish = [0] * self.problem.jobs
        for operation in operations:
            finish[operation.job] = max(finish[operation.job], operation.end_minute)
        return finish

    def _cost(self, operations: list[ScheduledOperation]) -> int:
        problem = self.problem
        finish = self._finish_minutes(operations)
        weighted = sum(int(problem.job_weight[job]) * max(0, finish[job] - int(problem.job_due[job]))
                       for job in range(problem.jobs))
        return problem.tardiness_scale * weighted + max(finish)

    def _outcomes(self, operations: list[ScheduledOperation]) -> pd.DataFrame:
        problem = self.problem
        finish = self._finish_minutes(operations)
        rows = []
        for job in range(problem.jobs):
            late = max(0, finish[job] - int(problem.job_due[job]))
            rows.append({"Zlecenie": problem.order_ids[job], "Produkt": problem.products[job],
                         "Priorytet": int(problem.job_weight[job]), "Napływ [min]": int(problem.job_arrival[job]),
                         "Termin [min]": int(problem.job_due[job]), "Koniec [min]": finish[job],
                         "Spóźnienie [min]": late, "Status": "spóźnione" if late else "na czas"})
        return pd.DataFrame(rows)

    def _operations(self, operations: list[ScheduledOperation]) -> pd.DataFrame:
        problem = self.problem
        return pd.DataFrame([{
            "Maszyna": problem.machine_labels[operation.machine],
            "Typ": problem.machine_labels[operation.machine][0],
            "Zlecenie": problem.order_ids[operation.job],
            "Produkt": problem.products[operation.job],
            "Krok": operation.step + 1,
            "Start [min]": operation.start_minute,
            "Koniec [min]": operation.end_minute,
        } for operation in operations])

    def _utilization(self, operations: pd.DataFrame, makespan: int) -> pd.DataFrame:
        problem = self.problem
        offsets = problem.type_machine_offset
        rows = []
        for index, name in enumerate(problem.machine_types):
            count = int(offsets[index + 1] - offsets[index])
            of_type = operations[operations["Typ"] == name]
            busy = int((of_type["Koniec [min]"] - of_type["Start [min]"]).sum())
            rows.append({"Maszyna": name, "Sztuk": count, "Zajętość [min]": busy,
                         "Wykorzystanie [%]": 100.0 * busy / (count * makespan)})
        return pd.DataFrame(rows)

    def _comparison_row(self, name: str, outcomes: pd.DataFrame) -> dict:
        late = outcomes["Spóźnienie [min]"]
        weighted = int((late * outcomes["Priorytet"]).sum())
        return {"Harmonogram": name, "Spóźnione zlecenia": int((late > 0).sum()),
                "Ważona spóźnialność [min]": weighted, "Suma spóźnień [min]": int(late.sum()),
                "Największe spóźnienie [min]": int(late.max()),
                "Koniec pracy [min]": int(outcomes["Koniec [min]"].max()),
                "Koszt": self.problem.tardiness_scale * weighted + int(outcomes["Koniec [min]"].max())}

    def report(self) -> dict:
        """One dictionary with everything the dashboard shows, per schedule name."""
        outcomes, operations, utilization, rows = {}, {}, {}, []
        for name, scheduled in self.all_schedules.items():
            outcomes[name] = self._outcomes(scheduled)
            operations[name] = self._operations(scheduled)
            makespan = int(outcomes[name]["Koniec [min]"].max())
            utilization[name] = self._utilization(operations[name], makespan)
            rows.append(self._comparison_row(name, outcomes[name]))
        return {"evolution_name": self.evolution_name, "names": list(self.all_schedules),
                "comparison": pd.DataFrame(rows), "outcomes": outcomes,
                "operations": operations, "utilization": utilization}
