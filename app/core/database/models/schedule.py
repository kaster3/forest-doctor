from datetime import datetime, timedelta

from sqlalchemy import BigInteger, ForeignKey, event
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.drug import Drug
from app.core.database.models.mixins import IntIdPkMixin
from app.core.database.models.user import User


class Schedule(IntIdPkMixin, Base):

    # Таймзона и время начала и окончания приема лекарства
    START_TIME = datetime.strptime("08:00", "%H:%M").time()
    END_TIME = datetime.strptime("22:00", "%H:%M").time()
    SINGLE_DOSE_TIME = datetime.strptime("14:00", "%H:%M").time()

    # Поля нашей модели
    taking_per_day: Mapped[int]
    duration: Mapped[int]
    schedule: Mapped[list[str]] = mapped_column(JSONB)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.policy", ondelete="CASCADE"),
    )
    drug_name: Mapped[str] = mapped_column(
        ForeignKey(
            "drugs.name",
            ondelete="CASCADE",
        )
    )
    # Связь (многие к одному)
    user: Mapped[User] = relationship(back_populates="schedules")
    drug: Mapped[Drug] = relationship(back_populates="schedules")

    def calculate_schedule(self) -> list[str]:
        schedule = []
        if self.taking_per_day == 1:
            schedule.append(self.SINGLE_DOSE_TIME.strftime("%H:%M"))
            return schedule

        start_time = datetime.combine(datetime.today(), self.START_TIME)
        end_time = datetime.combine(datetime.today(), self.END_TIME)
        interval_minutes = self.__calculate_interval(start_time, end_time)
        current_time = start_time

        while current_time <= end_time:
            schedule.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=interval_minutes)
            # Округляем минуты до ближайших 15
            if current_time.minute % 15 != 0:
                current_time = current_time.replace(minute=(current_time.minute // 15) * 15)
        return schedule

    def __calculate_interval(self, start_time, end_time) -> float:
        total_minutes = (end_time - start_time).total_seconds() / 60
        interval_minutes = total_minutes / (self.taking_per_day - 1)
        return interval_minutes


# Добавил событие, чтобы при создании модели сразу рассчитывать расписание на день, как поле
@event.listens_for(Schedule, "before_insert")
def calculate_schedule_before_insert(mapper, connection, target):
    target.schedule = target.calculate_schedule()
