"""create shifs table

Revision ID: 2f1f2d0293ca
Revises: 8942418f4c10
Create Date: 2026-01-26 22:12:17.901189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f1f2d0293ca'
down_revision: Union[str, Sequence[str], None] = '8942418f4c10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "shifts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("shifts")
