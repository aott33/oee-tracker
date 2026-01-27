"""create production runs table

Revision ID: 3dafd82ec639
Revises: 37afb0104629
Create Date: 2026-01-27 07:37:07.300535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dafd82ec639'
down_revision: Union[str, Sequence[str], None] = '37afb0104629'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "production_runs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("machine_id", sa.Integer, sa.ForeignKey("machines.id", ondelete="CASCADE")),
        sa.Column("shift_id", sa.Integer, sa.ForeignKey("shifts.id", ondelete="CASCADE")),
        sa.Column("operator_id", sa.Integer, sa.ForeignKey("operators.id", ondelete="CASCADE")),
        sa.Column("planned_start_time", sa.TIMESTAMP, nullable=False),
        sa.Column("planned_end_time", sa.TIMESTAMP, nullable=False),
        sa.Column("actual_start_time", sa.TIMESTAMP),
        sa.Column("actual_end_time", sa.TIMESTAMP),
        sa.Column("good_parts_count", sa.Integer),
        sa.Column("rejected_parts_count", sa.Integer)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("production_runs")