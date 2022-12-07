from pydantic import BaseModel
from task_admin.auth.schemas import UserSchema
from task_admin.tasks.models import TaskStatus


class TaskBaseSchema(BaseModel):
    title: str
    description: str
    status: TaskStatus
    assignee: UserSchema


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    user_id: int


class TaskUpdateSchema(BaseModel):
    title: str
    description: str
    status: TaskStatus
    user_id: int


class TaskSchema(TaskBaseSchema):
    id: int

    class Config:
        orm_mode = True
        use_enum_values = True
