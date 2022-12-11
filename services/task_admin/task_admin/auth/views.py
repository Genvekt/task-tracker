from task_admin.db.connection import get_db
from task_admin.db.repository import UserRepository
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from task_admin.auth.models import User
from task_admin.auth.schemas import UserSchema

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserSchema])
async def task_list(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return user_repo.list()
