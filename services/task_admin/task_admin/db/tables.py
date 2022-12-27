from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, MetaData, BigInteger, String, Column, ForeignKey

from task_admin.db.types import StrEnum
from task_admin.tasks.models import TaskStatus

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("public_id", String(100), unique=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True)
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(500), nullable=True),
    Column("status", StrEnum(TaskStatus), nullable=False),
    Column("user_id", BigInteger, ForeignKey("users.id"), nullable=True),
)
