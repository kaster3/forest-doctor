"""create schedules table

Revision ID: 259132a0d47a
Revises: e40943640c0c
Create Date: 2025-03-20 06:50:17.073748

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "259132a0d47a"
down_revision: Union[str, None] = "e40943640c0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("drug_name", sa.String(length=50), nullable=False),
        sa.Column("taking_per_day", sa.Integer(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("schedule", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["drug_name"],
            ["drugs.name"],
            name=op.f("fk_schedules_drug_name_drugs"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.policy"],
            name=op.f("fk_schedules_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedules")),
    )


def downgrade() -> None:
    op.drop_table("schedules")
