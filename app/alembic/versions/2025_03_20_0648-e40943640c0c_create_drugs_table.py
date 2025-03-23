"""create drugs table

Revision ID: e40943640c0c
Revises: 0173a0318f95
Create Date: 2025-03-20 06:48:47.903631

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e40943640c0c"
down_revision: Union[str, None] = "0173a0318f95"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "drugs",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("name", name=op.f("pk_drugs")),
    )


def downgrade() -> None:
    op.drop_table("drugs")
