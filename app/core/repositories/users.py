from abc import abstractmethod
from typing import Protocol

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.core.database import User
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

    async def create(self, policy) -> User | None:
        try:
            user = User(policy=policy)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": f"Patient with policy № {policy} already exists"},
            )

        return user

    async def get_by_policy(self, policy: int) -> User | None:
        user = await self.session.get(User, policy)
        return user
