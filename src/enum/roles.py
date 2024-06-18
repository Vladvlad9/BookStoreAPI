from enum import StrEnum

__all__ = ['UserRole']


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
