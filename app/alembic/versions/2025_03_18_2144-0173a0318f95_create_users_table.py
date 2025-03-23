"""create users table

Revision ID: 0173a0318f95
Revises:
Create Date: 2025-03-18 21:44:29.859952

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0173a0318f95"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("policy", sa.BigInteger(), nullable=False),
        sa.CheckConstraint(
            "policy < 10000000000000000",
            name=op.f("ck_users_check_id_max_length"),
        ),
        sa.CheckConstraint(
            "policy > 999999999999999",
            name=op.f("ck_users_check_id_min_length"),
        ),
        sa.PrimaryKeyConstraint("policy", name=op.f("pk_users")),
    )


def downgrade() -> None:
    op.drop_table("users")
