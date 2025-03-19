from typing import AsyncGenerator

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.db_helper import DataBaseHelper
from app.core.repositories.schedule import IScheduleRepository, ScheduleRepository
from app.core.repositories.users import IUserRepository, UserRepository
from app.core.settings import Settings
from app.core.use_cases.schedules import CreateScheduleInterator
from app.core.use_cases.users import CreateUserInteractor


class SQLAlchemyProvider(Provider):
    scope = Scope.APP
    settings = from_context(Settings)

    @provide
    async def get_database_helper(
        self,
        settings: Settings,
    ) -> DataBaseHelper:
        return DataBaseHelper(
            url=str(settings.db.url),
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self,
        database_helper: DataBaseHelper,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with database_helper.session_factory() as session:
            yield session


class UseCasesProvider(Provider):
    scope = Scope.REQUEST
    user_repository = provide(IUserRepository, provides=UserRepository)
    create_user = provide(CreateUserInteractor)

    schedule_repository = provide(IScheduleRepository, provides=ScheduleRepository)
    create_schedule = provide(CreateScheduleInterator)
