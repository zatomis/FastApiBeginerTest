"""Data base users

Revision ID: b26a0f39866d
Revises: e3b164c722b1
Create Date: 2024-12-06 13:27:10.982062

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b26a0f39866d"
down_revision: Union[str, None] = "e3b164c722b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("password"),
    )
    op.create_unique_constraint(None, "hotels", ["id"])
    op.alter_column(
        "rooms",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.SmallInteger(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.create_unique_constraint(None, "rooms", ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "rooms", type_="unique")
    op.alter_column(
        "rooms",
        "id",
        existing_type=sa.SmallInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.drop_constraint(None, "hotels", type_="unique")
    op.drop_table("users")
