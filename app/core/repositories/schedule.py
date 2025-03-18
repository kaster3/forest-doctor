from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select

from app.api.api_v1.schedules.schemas import ScheduleCreateRequest
from app.core.database.models.schedule import Schedule
from app.core.repositories.base import Repository


class ScheduleRepository(Protocol):

    @abstractmethod
    async def create(self, schedule_in: ScheduleCreateRequest) -> Schedule:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_policy(self, policy: int) -> list[Schedule]:
        """
        Возвращаем список всех id класса Schedule на основе полиса пациента,
        которые привязаны к нему
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, schedule_id: int, police: int) -> list[Schedule]:
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

    async def create(self, schedule_in: ScheduleCreateRequest) -> Schedule:
        schedule = Schedule(**schedule_in.model_dump())
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        return schedule

    async def get_all_by_policy(self, policy: int) -> list[Schedule]:
        stmt = select(Schedule).where(Schedule.user_id == policy)
        schedule = await self.session.scalars(stmt)
        return list(schedule)

    async def get_by_id(self, schedule_id: int, policy: int) -> list[Schedule]:
        pass
