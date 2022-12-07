from enum import Enum
from task_admin.auth.models import User


class TaskStatus(Enum):
    in_progress = "In Progress"
    done = "Done"


class Task:
    def __init__(
            self,
            title: str,
            description: str,
            assignee: User,
            status: TaskStatus = TaskStatus.in_progress
    ):
        """Single task initialization."""
        self.title = title
        self.description = description
        self.status = status
        self.assignee = assignee

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__),
            other.title == self.title,
            other.description == self.description,
            other.status == self.status,
            other.assignee == self.assignee
        )

    def close(self) -> None:
        """Mark task as Done."""
        if self.status != TaskStatus.done:
            self.status = TaskStatus.done
