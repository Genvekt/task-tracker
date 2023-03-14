from typing import Optional, List

from auth.models import User
from auth.models import Role


class RoleRepository:
    def __init__(self, session):
        self.session = session
        self.admin_role = "admin"

    def add(self, role: Role) -> None:
        self.session.add(role)

    def add_admin(self) -> Role:
        role = Role(name=self.admin_role)
        self.session.add(role)
        return role

    def get(self, name: str) -> Optional[Role]:
        return self.session.query(Role).where(Role.name == name).first()

    def get_admin(self) -> Optional[Role]:
        return self.session.query(Role).where(Role.name == self.admin_role).first()

    def list(self) -> List[Role]:
        return self.session.query(Role).all()


class UserRepository:
    def __init__(self, session):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    def get(self, email: str = "", id: int = 0) -> Optional[User]:
        if id > 0:
            return self.session.query(User).filter_by(id=id).first()
        else:
            return self.session.query(User).where(User.email == email).order_by(User.email).first()

    def list(self) -> List[User]:
        return self.session.query(User).all()
