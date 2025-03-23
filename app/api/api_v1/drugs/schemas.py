from pydantic import BaseModel, Field


class DrugBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=70)


class DrugCreate(DrugBase):
    pass
