"""create downtime events table

Revision ID: b08e271247b6
Revises: 3dafd82ec639
Create Date: 2026-01-27 07:46:32.382858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b08e271247b6'
down_revision: Union[str, Sequence[str], None] = '3dafd82ec639'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "downtime_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("production_run_id", sa.Integer, sa.ForeignKey("production_runs.id", ondelete="CASCADE")),
        sa.Column("reason_code", sa.String, sa.ForeignKey("reason_codes.code", ondelete="CASCADE")),
        sa.Column("start_time", sa.TIMESTAMP),
        sa.Column("end_time", sa.TIMESTAMP),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("downtime_events")
