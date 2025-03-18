from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.api_v1.users.schemas import UserCreate
from app.core.use_cases.users import CreateUserInteractor

router = APIRouter(prefix="/users", tags=["users"])


# http://localhost:8000/api/v1/users
@router.post(
    "/",
    response_model=UserCreate,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(user_in: UserCreate, interactor: FromDishka[CreateUserInteractor]):
    user = await interactor(user_in=user_in)
    return user


# http://localhost:8000/api/v1/users/next_takings?user_id=
@router.get("/next_takings/{user_id}")
async def get_next_takings(
    user_id: int,
):
    pass
