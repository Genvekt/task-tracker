from typing import Optional, List

from task_admin.tasks.models import Task


class TaskRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task: Task) -> None:
        self.session.add(task)

    def get(self, id: int) -> Optional[Task]:
        return self.session.query(Task).filter_by(id=id).first()

    def list(self)-> List[Task]:
        return self.session.query(Task).all()
