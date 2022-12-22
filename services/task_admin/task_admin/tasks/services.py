from sqlalchemy.orm import Session
from task_admin.db.repository import TaskRepository, UserRepository
import random

from task_admin.tasks.models import Task


def reassign_open_tasks(db: Session):
    task_repo = TaskRepository(db)
    open_tasks: list[Task] = task_repo.list_open()

    user_repo = UserRepository(db)
    users = user_repo.list()

    for task in open_tasks:
        lucky_user = random.choice(users)
        task.assignee = lucky_user

