from datetime import datetime

from pydantic import BaseModel

from accounting.auth.schemas import UserSchema
from accounting.transaction.models import TransactionType


class TransactionSchema(BaseModel):
    user: UserSchema
    type: TransactionType
    amount: float
    ts: datetime
    extra: dict

    class Config:
        orm_mode = True
        use_enum_values = True


class TransactionListSchema(BaseModel):
    collection: list[TransactionSchema]

    class Config:
        orm_mode = True
