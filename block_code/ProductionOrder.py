from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionOrder:
    """One order from the stream: make this product, within this time of its arrival."""

    order_id: str
    product: str
    arrival_minute: int
    deadline_minutes: int
    weight: int

    @property
    def due_minute(self) -> int:
        return self.arrival_minute + self.deadline_minutes
