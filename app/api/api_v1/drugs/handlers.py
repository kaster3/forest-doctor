from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.api_v1.drugs.schemas import DrugBase, DrugCreate
from app.core.use_cases.drugs import CreateDrugInteractor, GetDrugsInTimeRangeInteractor

router = APIRouter(prefix="/drugs", tags=["drugs"])


# http://localhost:8000/api/v1/drugs
@router.post(
    "/",
    response_model=DrugCreate,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_drug(
    drug_in: DrugCreate,
    interactor: FromDishka[CreateDrugInteractor],
):
    return await interactor(drug_in=drug_in)


# http://localhost:8000/api/v1/drugs/next_takings?user_id=
@router.get(
    path="/next_takings/{user_id}",
    response_model=list[DrugBase | None],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_drugs_in_time_range(
    user_id: int,
    interactor: FromDishka[GetDrugsInTimeRangeInteractor],
):
    return await interactor(user_id=user_id)
