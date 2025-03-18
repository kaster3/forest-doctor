import logging

from fastapi import HTTPException, status

from app.api.api_v1.schedules.schemas import ScheduleCreateRequest
from app.core.database.models.schedule import Schedule
from app.core.repositories.schedule import ScheduleRepository
from app.core.repositories.users import UserRepository

log = logging.getLogger(__name__)


class BaseScheduleInterator:
    def __init__(self, schedule_repository: ScheduleRepository) -> None:
        self.schedule_repository = schedule_repository


class CreateScheduleInterator(BaseScheduleInterator):
    def __init__(
        self, schedule_repository: ScheduleRepository, user_repository: UserRepository
    ) -> None:
        super().__init__(schedule_repository=schedule_repository)
        self.user_repository = user_repository

    async def __call__(self, schedule_in: ScheduleCreateRequest) -> Schedule:
        user = await self.user_repository.get_by_policy(policy=schedule_in.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Patient with policy № �� {schedule_in.user_id} not found",
            )
        schedule = await self.schedule_repository.create(schedule_in=schedule_in)
        log.info("Schedule with patient's policy № %s created successfully" % schedule.user_id)
        return schedule
