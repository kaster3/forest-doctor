import logging
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.api.api_v1.drugs.schemas import DrugCreate
from app.core.database import Drug
from app.core.exceptions import DrugAlreadyExistsError
from app.core.repositories.drug import DrugRepository
from app.core.repositories.schedule import ScheduleRepository
from app.core.use_cases.users import GetUserByPolicyInteractor

log = logging.getLogger(__name__)


class BaseDrugInteractor:
    def __init__(
        self,
        drug_repository: DrugRepository,
    ) -> None:
        self.drug_repository = drug_repository


class GetUserScheduleRepoDrugInteractor(BaseDrugInteractor):
    def __init__(
        self,
        drug_repository: DrugRepository,
        get_user_interactor: GetUserByPolicyInteractor,
        schedule_repository: ScheduleRepository,
    ) -> None:
        super().__init__(drug_repository)
        self.get_user_interactor = get_user_interactor
        self.schedule_repository = schedule_repository


class CreateDrugInteractor(BaseDrugInteractor):
    async def __call__(self, drug_in: DrugCreate) -> Drug:
        try:

            drug = await self.drug_repository.create(name=drug_in.name)
            log.info("Drug with name №% s created successfully" % drug_in.name)
            return drug

        except DrugAlreadyExistsError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": str(error)},
            )


class GetDrugByNameInteractor(BaseDrugInteractor):
    async def __call__(self, name: str) -> Drug | None:
        drug = await self.drug_repository.get_by_name(name=name)
        if not drug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Drug with {name} not found",
            )
        return drug


class GetDrugsInTimeRangeInteractor(GetUserScheduleRepoDrugInteractor):
    def __init__(
        self,
        drug_repository: DrugRepository,
        get_user_interactor: GetUserByPolicyInteractor,
        schedule_repository: ScheduleRepository,
        range_time: int,
    ) -> None:
        super().__init__(drug_repository, get_user_interactor, schedule_repository)
        self.range_time = range_time

    async def __call__(self, user_id: int) -> list[Drug | None]:
        now = datetime.now()
        one_hour_later = now + timedelta(hours=self.range_time)
        # я понимаю, что использую лишний запрос, но я не знаю, как по другому
        # сообщить пользователю, что юзера вообще нет
        await self.get_user_interactor(policy=user_id)
        schedules = await self.schedule_repository.get_all_by_policy(policy=user_id)
        drug_names = []
        for schedule in schedules:
            for time in schedule.schedule:
                schedule_datetime = datetime.strptime(time, "%H:%M").time()
                schedule_datetime_full = datetime.combine(now.date(), schedule_datetime)
                if now <= schedule_datetime_full <= one_hour_later:
                    drug_names.append(schedule.drug_name)
        drugs = [await self.drug_repository.get_by_name(name=drug_name) for drug_name in drug_names]

        return drugs
