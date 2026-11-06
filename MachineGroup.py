from dataclasses import dataclass


@dataclass(frozen=True)
class MachineGroup:
    """A type of machine and how many identical machines of it the factory has."""

    name: str
    count: int
