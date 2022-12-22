from datetime import datetime

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class RoleBaseSchema(BaseModel):
    name: str


class RoleSchema(RoleBaseSchema):
    class Config:
        orm_mode = True


class UserBaseSchema(BaseModel):
    name: str
    email: str
    roles: list[RoleSchema]


class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    roles: list[str]


class UserSchema(UserBaseSchema):
    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserSchema

    class Config:
        orm_mode = True


class PublicKey(BaseModel):
    alg: str
    use: str
    kid: str
    kty: str
    n: str
    e: str


class JWK(BaseModel):
    keys: list[PublicKey]
