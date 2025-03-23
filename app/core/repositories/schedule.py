from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

from asyncpg import ForeignKeyViolationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database.models.schedule import Schedule
from app.core.exceptions import DrugNotFoundError, UserNotFoundError
from app.core.repositories.base import Repository

if TYPE_CHECKING:
    from app.api.api_v1.schedules.schemas import ScheduleCreateRequest


class ScheduleRepository(Protocol):

    @abstractmethod
    async def create(self, schedule_in: "ScheduleCreateRequest") -> Schedule:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_policy(self, policy: int) -> list[Schedule]:
        """
        Возвращаем список всех id класса Schedule на основе полиса пациента,
        которые привязаны к нему
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, user_policy: int, schedule_id: int) -> Schedule | None:
        """
        Возвращает данные о выбранном расписании с рассчитанным графиком приёмов на день,
        на основе id расписания и полиса пациента
        """
        raise NotImplementedError


class IScheduleRepository(Repository):
    """
    Класс, реализующий интерфейс ScheduleRepository, для работы с Schedule моделью,
    наследуем init от Repository для получения сессии
    """

    async def create(self, schedule_in: "ScheduleCreateRequest") -> Schedule:
        try:

            schedule = Schedule(**schedule_in.model_dump())
            self.session.add(schedule)
            await self.session.commit()
            await self.session.refresh(schedule)
            return schedule

        except IntegrityError as error:
            error_message = str(error.orig).lower()
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                if "drugs" in error_message:
                    raise DrugNotFoundError(schedule_in.drug_name) from error
                elif "users" in error_message:
                    raise UserNotFoundError(schedule_in.user_id) from error

    async def get_all_by_policy(self, policy: int) -> list[Schedule]:
        stmt = select(Schedule).where(Schedule.user_id == policy)
        schedule = await self.session.scalars(stmt)
        return list(schedule)

    async def get_by_ids(
        self,
        user_policy: int,
        schedule_id: int,
    ) -> Schedule | None:
        stmt = select(Schedule).where(Schedule.id == schedule_id, Schedule.user_id == user_policy)
        schedule = await self.session.scalar(stmt)
        return schedule
