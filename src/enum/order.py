from enum import StrEnum

__all__ = ['OrderStatus']


class OrderStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
