from enum import Enum
from typing import Optional

from task_admin.auth.models import User


class TaskStatus(Enum):
    in_progress = "In Progress"
    done = "Done"


class Task:
    def __init__(
            self,
            title: str,
            description: str,
            assignee: Optional[User],
            status: TaskStatus = TaskStatus.in_progress
    ):
        """Single task initialization."""
        self.title = title
        self.description = description
        self.status = status
        self.assignee = assignee

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.title == self.title
            and other.description == self.description
            and other.status == self.status
            and (
                (other.assignee is None and self.assignee is None)
                or other.assignee == self.assignee
            )
        )

    def close(self) -> None:
        """Mark task as Done."""
        if self.status != TaskStatus.done:
            self.status = TaskStatus.done
