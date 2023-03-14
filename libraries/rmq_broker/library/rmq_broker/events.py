from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Event:
    """Base event class"""


@dataclass
class UserCreatedEvent(Event):
    public_id: str
    name: str
    email: str


@dataclass
class TaskCompletedEvent(Event):
    title: str
    description: str
    assignee_public_id: str
    ts: datetime


@dataclass
class TaskAssignedEvent(Event):
    title: str
    description: str
    assignee_public_id: str
    ts: datetime


@dataclass
class AccountSummary(Event):
    user_email: str
    date: date
    amount: float
