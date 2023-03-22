import asyncio
import uuid

from library.rmq_broker.events import UserCreatedEvent
from auth.broker.connection import publisher_event_queue
from auth.db.connection import get_db
from auth.db.repositories import UserRepository, RoleRepository
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.models import User
from auth.schemas import TokenSchema, UserSchema, UserCreateSchema, UserUpdateSchema, JWK
from auth.services.hash import verify_password
from auth.services.token import create_access_token, generate_jwk, get_jwk_fingerprint
from auth.services.user import add_user, authenticate_user, authenticate_admin_user
from auth.settings import ACCESS_TOKEN_EXPIRES

user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

auth_router = APIRouter(
    prefix="",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@user_router.get("/", response_model=list[UserSchema])
async def user_list(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    auth_user = authenticate_admin_user(token=token, db=db)
    if auth_user is None:
        raise HTTPException(status_code=403)

    user_repo = UserRepository(db)
    return user_repo.list()


@user_router.post("/")
async def user_create(
        data: UserCreateSchema,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    auth_user = authenticate_admin_user(token=token, db=db)
    if auth_user is None:
        raise HTTPException(status_code=403)

    await add_user(
        name=data.name,
        email=data.email,
        password=data.password,
        roles=[],
        db=db,
    )

    return "0k", 200


@user_router.get("/{user_id}", response_model=UserSchema)
async def user_get(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    auth_user = authenticate_admin_user(token=token, db=db)
    if auth_user is None:
        raise HTTPException(status_code=403)
    user_repo = UserRepository(db)
    user = user_repo.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@user_router.put("/{user_id}")
async def user_update(
    user_id: int,
    data: UserUpdateSchema,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    auth_user = authenticate_admin_user(token=token, db=db)
    if auth_user is None:
        raise HTTPException(status_code=403)
    user_repo = UserRepository(db)
    user = user_repo.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    role_repo = RoleRepository(db)
    new_roles = []
    for role in data.roles:
        role_db = role_repo.get(name=role)
        if role_db is None:
            raise HTTPException(status_code=404, detail=f"Role '{role}' not found.")
        new_roles.append(role_db)
    user.roles = new_roles
    db.commit()
    return "Ok", 200


@auth_router.post("/login", response_model=TokenSchema)
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get(email=data.username)

    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(plain_password=data.password, hashed_password=user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(
        username=user.email,
        roles=[role.name for role in user.roles],
        expires_delta=ACCESS_TOKEN_EXPIRES,
    )
    token.user = user
    return token


@auth_router.post("/authenticate", response_model=UserSchema)
async def authenticate(encoded_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = authenticate_user(token=encoded_token, db=db)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid auth token.")

    return user


@auth_router.get("/jwk.json", response_model=JWK)
def jwk_json():
    #print(get_jwk_fingerprint())
    jwk_dict = generate_jwk()
    return {"keys": [jwk_dict]}
