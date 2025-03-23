import logging

from fastapi import HTTPException, status

from app.api.api_v1.schedules.schemas import ScheduleCreateRequest
from app.core.database.models.schedule import Schedule
from app.core.exceptions import DrugNotFoundError, UserNotFoundError
from app.core.repositories.schedule import ScheduleRepository
from app.core.use_cases.users import GetUserByPolicyInteractor

log = logging.getLogger(__name__)


class BaseScheduleInterator:
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
    ) -> None:
        self.schedule_repository = schedule_repository


class GetUserScheduleInterator(BaseScheduleInterator):
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        get_user_interactor: GetUserByPolicyInteractor,
    ) -> None:
        super().__init__(schedule_repository)
        self.get_user_interactor = get_user_interactor


class CreateScheduleInterator(BaseScheduleInterator):
    async def __call__(self, schedule_in: ScheduleCreateRequest) -> Schedule:
        try:
            schedule = await self.schedule_repository.create(schedule_in=schedule_in)
        except DrugNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": f"Drug '{schedule_in.drug_name}' not found"},
            )
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": f"User with policy '{schedule_in.user_id}' not found"},
            )

        log.info("Schedule with patient's policy № %s created successfully" % schedule.user_id)
        return schedule


class GetSchedulesByPolicy(GetUserScheduleInterator):
    async def __call__(self, user_policy: int) -> list[int]:
        # я понимаю, что использую лишний запрос, но я не знаю, как по другому
        # сообщить пользователю, что юзера вообще нет
        await self.get_user_interactor(user_policy)
        schedules = await self.schedule_repository.get_all_by_policy(policy=user_policy)
        schedules_id = [schedules.id for schedules in schedules]
        return schedules_id


class GetScheduleByIdsInteractor(BaseScheduleInterator):
    async def __call__(self, user_policy: int, schedule_id: int) -> Schedule | None:
        schedule = await self.schedule_repository.get_by_ids(
            schedule_id=schedule_id,
            user_policy=user_policy,
        )
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule № {schedule_id} not found for patient with policy {user_policy}",
            )
        return schedule
