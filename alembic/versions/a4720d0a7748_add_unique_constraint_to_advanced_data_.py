"""add unique constraint to advanced_data upc

Revision ID: a4720d0a7748
Revises: ff6cdd6598d0
Create Date: 2026-08-11 10:51:04.450372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4720d0a7748'
down_revision: Union[str, Sequence[str], None] = 'ff6cdd6598d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_advanced_data_upc",
        "advanced_data",
        ["upc"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_unique_constraint(
        "uq_advanced_data_upc",
        "advanced_data",
        type = "unique",
    )
