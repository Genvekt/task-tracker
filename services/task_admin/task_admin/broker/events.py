from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TaskCompletedEvent:
    title: str
    description: str
    assignee_public_id: str
    ts: datetime

    def dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "assignee_public_id": self.assignee_public_id,
            "ts": self.ts.isoformat(),
        }


@dataclass
class TaskAssignedEvent:
    title: str
    description: str
    assignee_public_id: str
    ts: datetime

    def dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "assignee_public_id": self.assignee_public_id,
            "ts": self.ts.isoformat(),
        }
