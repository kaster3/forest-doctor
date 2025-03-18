from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.api_v1.schedules.schemas import ScheduleCreateRequest, ScheduleCreateResponse
from app.core.use_cases.schedules import CreateScheduleInterator
from app.core.use_cases.users import CreateUserInteractor

router = APIRouter(tags=["schedules"])


#  http://localhost:8000/api/v1/schedule
@router.post(
    path="/schedule",
    response_model=ScheduleCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_schedule(
    schedule_in: ScheduleCreateRequest, interactor: FromDishka[CreateScheduleInterator]
):
    return await interactor(schedule_in=schedule_in)


#  http://localhost:8000/api/v1/schedules?user_id=
@router.get(
    "/schedules/{user_policy}",
    response_model=list[int],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_schedules_by_policy(user_policy: int, interactor: FromDishka[CreateUserInteractor]):
    pass


#  http://localhost:8000/api/v1/schedule?user_id=&schedule_id=
@router.get(
    "/schedule/{user_policy}/{schedule_id}",
    response_model=ScheduleCreateResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_schedule_by_policy_and_id(
    user_policy: int,
    schedule_id: int,
    interactor: FromDishka[CreateUserInteractor],
):
    pass
