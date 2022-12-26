from pydantic.main import BaseModel


class UserBaseSchema(BaseModel):
    public_id: str
    name: str
    email: str


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True
