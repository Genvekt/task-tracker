from pydantic.main import BaseModel


class UserBaseSchema(BaseModel):
    name: str


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True