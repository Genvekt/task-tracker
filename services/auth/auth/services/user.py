import uuid
from typing import Optional
from sqlalchemy.orm import Session

from jwt import DecodeError

from auth.broker.connection import publisher_event_queue
from auth.db.connection import SessionLocal

from auth.db.repositories import UserRepository, RoleRepository
from auth.models import Role, User
from auth.services.token import decode_token
from auth.settings import ADMIN_PASSWORD
from library.rmq_broker.events import UserCreatedEvent


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


async def add_admin_user(db: Session):
    role_repo = RoleRepository(db)
    admin_role = role_repo.get_admin()
    if admin_role is None:
        admin_role = role_repo.add_admin()

    await add_user(
        name="Admin",
        email="admin@email.com",
        password=ADMIN_PASSWORD,
        roles=[admin_role],
        db=db,
    )
    db.commit()


async def add_user(name: str, email: str, password: str, roles: list[Role], db: Session):
    user_repo = UserRepository(db)
    if user_repo.get(email=email) is not None:
        # User already exists
        return None

    user = User(
        public_id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=password
    )
    user_repo.add(user)
    user.roles = roles
    db.commit()

    # Notify that new user was added
    await publisher_event_queue.put(UserCreatedEvent(
        public_id=user.public_id,
        name=user.name,
        email=user.email,
    ))

    return user
