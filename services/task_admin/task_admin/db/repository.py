from typing import Optional, List

from task_admin.auth.models import User
from task_admin.tasks.models import Task, TaskStatus


class TaskRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task: Task) -> None:
        self.session.add(task)

    def get(self, id: int) -> Optional[Task]:
        return self.session.query(Task).filter_by(id=id).first()

    def list_open(self) -> List[Task]:
        return self.session.query(Task).filter_by(status=TaskStatus.in_progress.value).all()

    def list(self) -> List[Task]:
        return self.session.query(Task).all()


class UserRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task: User) -> None:
        self.session.add(task)

    def get(self, email: str = "", id: int = 0) -> Optional[User]:
        if id > 0:
            return self.session.query(User).filter_by(id=id).first()
        else:
            return self.session.query(User).where(User.email == email).first()

    def list(self) -> List[User]:
        return self.session.query(User).all()
