import logging

from fastapi import HTTPException, status

from app.api.api_v1.users.schemas import UserCreate
from app.core.database import User
from app.core.exceptions import UserAlreadyExistsError
from app.core.repositories.users import UserRepository

log = logging.getLogger(__name__)


class BaseUserInteractor:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


class CreateUserInteractor(BaseUserInteractor):
    async def __call__(self, user_in: UserCreate) -> User:
        try:
            user = await self.user_repository.create(policy=user_in.policy)
            log.info("Patient with policy №% s created successfully" % user.policy)
            return user

        except UserAlreadyExistsError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": str(error)},
            )


class GetUserByPolicyInteractor(BaseUserInteractor):
    async def __call__(self, policy: int) -> User | None:
        user = await self.user_repository.get_by_policy(policy=policy)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with policy № {policy} not found",
            )
        return user
