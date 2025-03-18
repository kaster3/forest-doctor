from pydantic import BaseModel


class UserBase(BaseModel):
    policy: int  # constr(min_length=16, max_length=16)


class UserCreate(UserBase):
    pass
