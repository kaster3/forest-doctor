from typing import Annotated

from pydantic import BaseModel, Field

UserPolicy = Annotated[int, Field(ge=1000000000000000, le=9999999999999999)]


class UserBase(BaseModel):
    policy: UserPolicy


class UserCreate(UserBase):
    pass
