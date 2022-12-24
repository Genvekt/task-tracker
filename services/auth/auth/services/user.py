import uuid
from typing import Optional
from sqlalchemy.orm import Session

from jwt import DecodeError

from auth.db.repositories import UserRepository, RoleRepository
from auth.models import User
from auth.services.token import decode_token
from auth.settings import ADMIN_PASSWORD


def authenticate_user(token: str, db: Session) -> Optional[User]:
    try:
        decoded_token = decode_token(token)
    except DecodeError:
        return None

    user_email = decoded_token.get("sub")
    if user_email is None:
        return None

    user_repo = UserRepository(db)
    return user_repo.get(email=user_email)


def authenticate_admin_user(token: str, db: Session) -> Optional[User]:
    user = authenticate_user(token=token, db=db)
    if user is None:
        return None

    admin_role = RoleRepository(db).get_admin()
    if admin_role not in user.roles:
        return None

    return user


def add_admin_user():
    from auth.db.connection import get_db
    db = next(get_db())
    user_repo = UserRepository(db)
    if user_repo.get(email="admin@email.com") is not None:
        # Admin already exists
        return

    user = User(
        public_id=str(uuid.uuid4()),
        name="Admin",
        email="admin@email.com",
        password=ADMIN_PASSWORD
    )

    role_repo = RoleRepository(db)
    admin_role = role_repo.get_admin()
    if admin_role is None:
        admin_role = role_repo.add_admin()

    user.roles.append(admin_role)
    user_repo.add(user)
    db.commit()
