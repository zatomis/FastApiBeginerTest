"""Add 2 table

Revision ID: 33c795e94456
Revises: 
Create Date: 2024-11-27 11:33:33.340480

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "33c795e94456"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "rooms",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("hotel_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
    op.drop_table("hotels")
