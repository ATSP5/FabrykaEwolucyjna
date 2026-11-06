from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduledOperation:
    """One recipe step of one order placed on a concrete machine at a concrete time."""

    job: int
    step: int
    machine: int
    start_minute: int
    end_minute: int
