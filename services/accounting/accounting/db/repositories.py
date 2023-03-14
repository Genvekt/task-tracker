from typing import Optional, List
from datetime import date, timedelta, datetime

from accounting.auth.models import User
from accounting.transaction.models import Transaction, TransactionType
from sqlalchemy.sql.functions import sum as sql_sum


class TransactionRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task: Transaction) -> None:
        self.session.add(task)

    def get(self, id: int) -> Optional[Transaction]:
        return self.session.query(Transaction).filter_by(id=id).first()

    def list(self, user: User = None, date: date = None) -> List[Transaction]:
        query = self.session.query(Transaction)
        if user is not None:
            query = query.filter_by(user=user)
        if date is not None:
            query = query.where(Transaction.ts > date, Transaction.ts < date + timedelta(days=1))
        return query.all()


class UserRepository:
    def __init__(self, session):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    def get(self, email: str = None, public_id: str = None, id: int = 0) -> Optional[User]:
        if id > 0:
            return self.session.query(User).filter_by(id=id).first()
        elif email is not None:
            return self.session.query(User).where(User.email == email).first()
        else:
            return self.session.query(User).where(User.public_id == public_id).first()

    def list(self) -> List[User]:
        return self.session.query(User).all()


class SalaryPaymentRepository:
    def __init__(self, session):
        self.session = session

    def list(self, date_: date) -> List[Transaction]:
        date_start = datetime.combine(date_, datetime.min.time())
        next_date_start = datetime.combine(date_+timedelta(days=1), datetime.min.time())

        result: tuple[User, float] = self.session.query(
            User,
            sql_sum(Transaction.amount)
        ).join(Transaction).where(
            Transaction.ts >= date_start,
            Transaction.ts < next_date_start
        ).group_by(User).all()

        return [
            Transaction(
                user=user,
                type_=TransactionType.salary_payment,
                ts=next_date_start,
                amount=amount
            )
            for user, amount in result
        ]

    def add(self, salary: Transaction):
        self.session.add(salary)
