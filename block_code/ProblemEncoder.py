import numpy as np

from FactoryProblem import FactoryProblem
from MachineGroup import MachineGroup
from ProductionOrder import ProductionOrder
from Recipe import Recipe


class ProblemEncoder:
    """Turns machines, recipes and orders into the flat int32 arrays the kernels work on."""

    MAX_JOBS = 512
    MAX_MACHINES = 64

    def __init__(self, machines: list[MachineGroup], recipes: list[Recipe], orders: list[ProductionOrder],
                 tardiness_scale: int = 100):
        if tardiness_scale < 1:
            raise ValueError("tardiness_scale must be at least 1")
        machine_count = sum(group.count for group in machines)
        if not orders or len(orders) > self.MAX_JOBS:
            raise ValueError("%d orders; the kernels take 1 to %d" % (len(orders), self.MAX_JOBS))
        if machine_count > self.MAX_MACHINES:
            raise ValueError("%d machines; the kernels take at most %d" % (machine_count, self.MAX_MACHINES))
        self._encoded = self._encode(machines, recipes, orders, tardiness_scale)

    def _encode(self, machines, recipes, orders, tardiness_scale) -> FactoryProblem:
        type_index = {group.name: index for index, group in enumerate(machines)}
        recipe_of = {recipe.product: recipe for recipe in recipes}
        offsets, types, minutes = [0], [], []
        for order in orders:
            for step in recipe_of[order.product].steps:
                types.append(type_index[step.machine])
                minutes.append(step.minutes)
            offsets.append(len(types))
        return FactoryProblem(
            machine_types=tuple(group.name for group in machines),
            machine_labels=tuple("%s%d" % (group.name, number + 1) for group in machines for number in range(group.count)),
            order_ids=tuple(order.order_id for order in orders),
            products=tuple(order.product for order in orders),
            job_op_offset=np.array(offsets, dtype=np.int32),
            op_machine_type=np.array(types, dtype=np.int32),
            op_minutes=np.array(minutes, dtype=np.int32),
            job_arrival=np.array([order.arrival_minute for order in orders], dtype=np.int32),
            job_due=np.array([order.due_minute for order in orders], dtype=np.int32),
            job_weight=np.array([order.weight for order in orders], dtype=np.int32),
            type_machine_offset=np.cumsum([0] + [group.count for group in machines], dtype=np.int32),
            tardiness_scale=tardiness_scale,
        )

    def problem(self) -> FactoryProblem:
        return self._encoded

    def job_op_offset(self) -> np.ndarray:
        return self._encoded.job_op_offset

    def op_machine_type(self) -> np.ndarray:
        return self._encoded.op_machine_type

    def op_minutes(self) -> np.ndarray:
        return self._encoded.op_minutes

    def job_arrival(self) -> np.ndarray:
        return self._encoded.job_arrival

    def job_due(self) -> np.ndarray:
        return self._encoded.job_due

    def job_weight(self) -> np.ndarray:
        return self._encoded.job_weight

    def type_machine_offset(self) -> np.ndarray:
        return self._encoded.type_machine_offset
