from pydantic.main import BaseModel


class UserSchema(BaseModel):
    id: int
    public_id: str
    name: str
    email: str

    class Config:
        orm_mode = True
