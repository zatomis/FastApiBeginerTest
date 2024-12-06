"""Добавил поле имя в БД users

Revision ID: 79c877ecb512
Revises: b26a0f39866d
Create Date: 2024-12-06 13:32:51.849508

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79c877ecb512"
down_revision: Union[str, None] = "b26a0f39866d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=100), nullable=False))
    op.alter_column(
        "users",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.SmallInteger(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.create_unique_constraint(None, "users", ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.alter_column(
        "users",
        "id",
        existing_type=sa.SmallInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.drop_column("users", "name")
