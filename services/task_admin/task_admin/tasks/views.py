from task_admin.db.connection import get_db
from task_admin.db.repository import TaskRepository
from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session

from task_admin.tasks.models import Task
from task_admin.tasks.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema, TaskListSchema
from task_admin.tasks.services import reassign_open_tasks

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=TaskListSchema)
async def task_list(db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    return {"collection": task_repo.list()}


@router.get("/{task_id}", response_model=TaskSchema)
async def task_get(task_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get(id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task is not found.")
    return task


@router.post("/", response_model=TaskSchema)
async def task_create(data: TaskCreateSchema, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = Task(
        title=data.title,
        description=data.description,
        assignee=None
    )
    task_repo.add(task)
    db.commit()

    return task


@router.put("/{task_id}", response_model=TaskSchema)
async def update_item(task_id: int, data: TaskUpdateSchema, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get(id=task_id)

    task.status = data.status
    db.commit()

    return task


@router.post("/reassign")
async def reassign_tasks(db: Session = Depends(get_db)):
    reassign_open_tasks(db=db)
    db.commit()

    return Response(status_code=200)
