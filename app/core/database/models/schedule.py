from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.mixins import IntIdPkMixin
from app.core.database.models.user import User


class Schedule(IntIdPkMixin, Base):

    drug_name: Mapped[str] = mapped_column(String(30))
    taking_per_day: Mapped[int]
    duration: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )

    # Связь с таблицей User (многие к одному)
    user: Mapped[User] = relationship(back_populates="schedules")
