from dataclasses import dataclass, asdict


@dataclass
class TaskCompletedEvent:
    title: str
    description: str
    assignee_public_id: str

    dict = asdict
