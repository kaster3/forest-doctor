from fastapi import APIRouter

from app.api.api_v1.drugs.handlers import router as drug_router
from app.api.api_v1.schedules.handlers import router as schedule_router
from app.api.api_v1.users.handlers import router as user_router
from app.core import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

for rout in (user_router, schedule_router, drug_router):
    router.include_router(
        router=rout,
    )


@router.get("")
async def root():
    return {"message": "this path is http://127.0.0.1:8000/api/v1"}
