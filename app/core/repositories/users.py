from abc import abstractmethod
from typing import Protocol

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.core.database import User
from app.core.exceptions import UserAlreadyExistsError
from app.core.repositories.base import Repository


class UserRepository(Protocol):
    @abstractmethod
    async def create(self, policy: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_policy(self, policy: int) -> User | None:
        raise NotImplementedError


class IUserRepository(Repository):
    """
    Класс, реализующий интерфейс UserRepository, для работы с User моделью,
    наследуем init от Repository для получения сессии
    """

    async def create(self, policy: int) -> User | None:
        user = User(policy=policy)
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as error:
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise UserAlreadyExistsError(f"Patient with policy № {policy} already exists")
        return user

    async def get_by_policy(self, policy: int) -> User | None:
        user = await self.session.get(User, policy)
        return user
