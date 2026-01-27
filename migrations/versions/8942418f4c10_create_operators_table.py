"""create operators table

Revision ID: 8942418f4c10
Revises: e994631454cb
Create Date: 2026-01-26 22:08:43.810448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8942418f4c10'
down_revision: Union[str, Sequence[str], None] = 'e994631454cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "operators",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("operators")
