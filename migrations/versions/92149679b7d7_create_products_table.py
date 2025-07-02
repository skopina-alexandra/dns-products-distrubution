"""create products table

Revision ID: 92149679b7d7
Revises: 66ff6c3759df
Create Date: 2025-07-01 23:30:23.670946

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '92149679b7d7'
down_revision: Union[str, Sequence[str], None] = '66ff6c3759df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text("""
    create table products(
        product_id uuid primary key,
        category_id uuid not null references categories(id) on delete restrict
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists products
    """)
    connection = op.get_bind()
    connection.execute(sql)
