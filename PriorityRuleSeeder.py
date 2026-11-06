import numpy as np

from FactoryProblem import FactoryProblem


class PriorityRuleSeeder:
    """Classic dispatching rules, each written as a chromosome: the baselines and the first seeds."""

    RULES = ("FIFO", "EDD", "SPT", "LST")

    def __init__(self, problem: FactoryProblem):
        self.problem = problem

    def seeds(self) -> dict[str, np.ndarray]:
        return {rule: self._dispatch(rule) for rule in self.RULES}

    def _priority(self, rule: str, job: int, op: int, start: int) -> int:
        problem = self.problem
        if rule == "FIFO":
            return int(problem.job_arrival[job])
        if rule == "EDD":
            return int(problem.job_due[job])
        if rule == "SPT":
            return int(problem.op_minutes[op])
        remaining = int(problem.op_minutes[op:problem.job_op_offset[job + 1]].sum())
        return int(problem.job_due[job]) - start - remaining

    def _dispatch(self, rule: str) -> np.ndarray:
        problem = self.problem
        next_op = problem.job_op_offset[:-1].tolist()
        last_op = problem.job_op_offset[1:].tolist()
        ready = problem.job_arrival.tolist()
        machine_free = [0] * problem.machines
        chromosome = []
        for _ in range(problem.genes):
            best = None
            for job in range(problem.jobs):
                op = next_op[job]
                if op == last_op[job]:
                    continue
                machine, start = problem.pick_machine(machine_free, int(problem.op_machine_type[op]), ready[job])
                key = (start, self._priority(rule, job, op, start), job)
                if best is None or key < best[0]:
                    best = (key, job, op, machine, start)
            _, job, op, machine, start = best
            end = start + int(problem.op_minutes[op])
            machine_free[machine] = end
            ready[job] = end
            next_op[job] = op + 1
            chromosome.append(job)
        return np.array(chromosome, dtype=np.int32)
