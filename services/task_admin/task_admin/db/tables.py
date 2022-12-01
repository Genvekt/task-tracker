from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, MetaData, Integer, String, Column, ForeignKey

from task_admin.db.types import StrEnum
from task_admin.tasks.models import TaskStatus

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False)
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(500), nullable=True),
    Column("status", StrEnum(TaskStatus), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)
