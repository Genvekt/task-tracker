from datetime import datetime
from enum import Enum

from accounting.auth.models import User

class TransactionType(Enum):
    task_assigned = "TaskAssigned"
    task_completed = "TaskCompleted"


class Transaction:
    def __init__(self, user: User, type_: TransactionType, amount: float, ts: datetime, extra: dict = None):
        if extra is None:
            extra = {}
        self.user = user
        self.type = type_
        self.amount = amount
        self.ts = ts
        self.extra = extra

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.user == self.user
            and other.type == self.type
            and other.amount == self.amount
            and other.ts == self.ts
            and other.extra == self.extra
        )
