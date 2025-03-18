import logging

from fastapi import HTTPException, status

from app.api.api_v1.users.schemas import UserCreate
from app.core.database import User
from app.core.repositories.users import UserRepository

log = logging.getLogger(__name__)


class CreateUserInteractor:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_in: UserCreate) -> User:
        self._check_policy(user_in.policy)
        user = await self.user_repository.create(policy=user_in.policy)
        log.info("Patient with policy №% s created successfully" % user.policy)
        return user

    @staticmethod
    def _check_policy(policy: int) -> None:
        policy_str = str(policy)
        if (quantity_digits := len(policy_str)) != 16:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Number of policy have to contains 16 digits, gotten {quantity_digits}",
            )
