from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base

if TYPE_CHECKING:
    from app.core.database.models.schedule import Schedule


class User(Base):
    policy: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    # Связь
    schedules: Mapped[list["Schedule"]] = relationship(back_populates="user")

    # Решил добавить проверку валидности полиса (id) на уровне бд, включительно
    __table_args__ = (
        CheckConstraint("policy > 999999999999999", name="check_id_min_length"),
        CheckConstraint("policy < 10000000000000000", name="check_id_max_length"),
    )
