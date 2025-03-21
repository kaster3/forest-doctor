from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base

if TYPE_CHECKING:
    from app.core.database.models.schedule import Schedule


class Drug(Base):
    """
    Решил сделать отдельную таблицу, хоть в задание сказано, что только имя используется,
    для будущего расширения информации о таблетках
    """

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    # Cвязи
    schedules: Mapped[list["Schedule"]] = relationship(back_populates="drug")
