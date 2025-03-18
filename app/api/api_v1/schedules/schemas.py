from pydantic import BaseModel


class ScheduleBase(BaseModel):
    pass


class ScheduleCreateRequest(ScheduleBase):
    drug_name: str
    taking_per_day: int
    duration: int
    user_id: int


class ScheduleCreateResponse(ScheduleBase):
    id: int
