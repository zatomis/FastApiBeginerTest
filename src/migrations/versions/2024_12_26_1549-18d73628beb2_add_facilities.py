"""Add facilities
Revision ID: 18d73628beb2
Revises: 72a85e07ec1a
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "18d73628beb2"
down_revision: Union[str, None] = "72a85e07ec1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("room_id", sa.SmallInteger(), nullable=False),
        sa.Column("facility_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_unique_constraint(None, "bookings", ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "bookings", type_="unique")
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
