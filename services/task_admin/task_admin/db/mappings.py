from sqlalchemy.orm import registry, relationship
from task_admin.auth.models import User
from task_admin.db.tables import users_table, tasks_table
from task_admin.tasks.models import Task

mapper_registry = registry()

mapper_registry.map_imperatively(
    User,
    users_table
)

mapper_registry.map_imperatively(
    Task,
    tasks_table,
    properties={
        "assignee": relationship(User, backref="users", lazy="joined")
    },
)
