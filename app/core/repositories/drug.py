from abc import abstractmethod
from typing import Protocol

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.core.database import Drug
from app.core.exceptions import DrugAlreadyExistsError
from app.core.repositories.base import Repository


class DrugRepository(Protocol):
    @abstractmethod
    async def create(self, name: str) -> Drug | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Drug | None:
        raise NotImplementedError


class IDrugRepository(Repository):
    """
    Класс, реализующий интерфейс DrugRepository, для работы с Drug моделью,
    наследуем init от Repository для получения сессии
    """

    async def create(self, name: str) -> Drug | None:
        drug = Drug(name=name)
        self.session.add(drug)
        try:
            await self.session.commit()
        except IntegrityError as error:
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise DrugAlreadyExistsError(f"Drug with name {name} already exists")
        return drug

    async def get_by_name(self, name: str) -> Drug | None:
        drug = await self.session.get(Drug, name)
        return drug
