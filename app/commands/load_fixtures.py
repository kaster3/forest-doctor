import asyncio
import json
import logging
from pathlib import Path

from app.api.api_v1.drugs.schemas import DrugCreate
from app.api.api_v1.schedules.schemas import ScheduleCreateRequest
from app.api.api_v1.users.schemas import UserCreate
from app.core.settings import Settings
from app.core.use_cases.drugs import CreateDrugInteractor
from app.core.use_cases.schedules import CreateScheduleInterator
from app.core.use_cases.users import CreateUserInteractor
from app.ioc.init_container import init_async_container

FIXTURES_PACKAGE_NAME = Path(__file__).parent.parent / "fixtures"
USER_FIXTURES_NAME = "users.json"
DRUGS_FIXTURES_NAME = "drugs.json"
SCHEDULES_FIXTURES_NAME = "schedules.json"

USERS_FIXTURES_PATH = FIXTURES_PACKAGE_NAME / USER_FIXTURES_NAME
DRUGS_FIXTURES_PATH = FIXTURES_PACKAGE_NAME / DRUGS_FIXTURES_NAME
SCHEDULES_FIXTURES_PATH = FIXTURES_PACKAGE_NAME / SCHEDULES_FIXTURES_NAME

load_info = {
    "users": {
        "fixtures_path": USERS_FIXTURES_PATH,
        "interactor_class": CreateUserInteractor,
        "schema": UserCreate,
    },
    "drugs": {
        "fixtures_path": DRUGS_FIXTURES_PATH,
        "interactor_class": CreateDrugInteractor,
        "schema": DrugCreate,
    },
    "schedules": {
        "fixtures_path": SCHEDULES_FIXTURES_PATH,
        "interactor_class": CreateScheduleInterator,
        "schema": ScheduleCreateRequest,
    },
}


async def main(settings: Settings) -> None:

    container = init_async_container(settings=settings)
    async with container() as request_container:
        for key, value in load_info.items():
            logging.info("Loading %s fixtures..." % key)
            interactor = await request_container.get(value.get("interactor_class"))
            with open(value.get("fixtures_path"), "r", encoding="utf-8") as file:
                data = json.load(file)
                # Тут можно было бы создать отдельные интеракторы для загрузки пачками, а не по 1,
                # но не уложился по времени
                for obj in data:
                    schema = value.get("schema")
                    schema_obj = schema(**obj)
                    await interactor(schema_obj)
            logging.info("%s's fixtures loaded successfully!" % key)
        logging.info("ALL fixtures loaded successfully!")


if __name__ == "__main__":
    settings = Settings()
    asyncio.run(main(settings=settings))
