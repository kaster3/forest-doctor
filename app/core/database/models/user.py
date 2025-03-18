from sqlalchemy import BigInteger, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.models.base import Base


class User(Base):
    policy: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Решил добавить проверку валидности полиса (id) на уровне бд, включительно
    __table_args__ = (
        CheckConstraint("policy > 999999999999999", name="check_id_min_length"),
        CheckConstraint("policy < 10000000000000000", name="check_id_max_length"),
    )
