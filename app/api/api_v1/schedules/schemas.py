from pydantic import BaseModel, Field

from app.api.api_v1.users.schemas import UserPolicy


class ScheduleBase(BaseModel):
    pass


class ScheduleCreateRequest(ScheduleBase):
    drug_name: str = Field(..., min_length=2)
    taking_per_day: int = Field(..., gt=0)
    duration: int = Field(..., gt=0)
    user_id: UserPolicy


class ScheduleCreateResponse(ScheduleBase):
    id: int


class ScheduleListResponse(ScheduleBase):
    schedule: list[str]
