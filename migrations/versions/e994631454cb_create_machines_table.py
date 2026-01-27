"""create machines table

Revision ID: e994631454cb
Revises: 
Create Date: 2026-01-26 21:52:44.157899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e994631454cb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "machines",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("ideal_cycle_time", sa.Float, nullable=False),
        sa.Column("location", sa.String)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("machines")
