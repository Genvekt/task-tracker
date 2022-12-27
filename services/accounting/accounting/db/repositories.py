from typing import Optional, List

from accounting.auth.models import User
from accounting.transaction.models import Transaction


class TransactionRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task: Transaction) -> None:
        self.session.add(task)

    def get(self, id: int) -> Optional[Transaction]:
        return self.session.query(Transaction).filter_by(id=id).first()

    def list(self) -> List[Transaction]:
        return self.session.query(Transaction).all()


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
