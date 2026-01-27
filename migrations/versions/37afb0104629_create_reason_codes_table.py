"""create reason codes table

Revision ID: 37afb0104629
Revises: d571592ac2c9
Create Date: 2026-01-27 07:33:55.840928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37afb0104629'
down_revision: Union[str, Sequence[str], None] = 'd571592ac2c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "reason_codes",
        sa.Column("code", sa.String, primary_key=True),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("is_planned", sa.Boolean, default=False)
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("reason_codes")
