from datetime import date

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from accounting.db.connection import get_db
from accounting.db.repositories import TransactionRepository, UserRepository
from accounting.transaction.schemas import TransactionListSchema

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"],
)


@router.get("/", response_model=TransactionListSchema)
async def task_list(
    user_public_id: str = None,
    date: date = None,
    db: Session = Depends(get_db)
):
    trans_repo = TransactionRepository(db)
    if user_public_id is None:
        return {"collection": trans_repo.list(date=date)}

    else:
        user_repo = UserRepository(db)
        user = user_repo.get(public_id=user_public_id)
        if user is None:
            return {"collection": []}
        else:
            return {"collection": trans_repo.list(user=user, date=date)}
