"""create dc_products table

Revision ID: 260d1de87be5
Revises: 4c8b06f3f3b2
Create Date: 2025-07-02 01:32:08.981817

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '260d1de87be5'
down_revision: Union[str, Sequence[str], None] = '4c8b06f3f3b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text("""
    create table dc_products(
        dc_id uuid not null references distribution_centers(id) on delete restrict,
        product_id uuid not null references products(product_id) on delete restrict,
        stock_quantity integer not null check (stock_quantity >= 0),
        reserve_quantity integer not null check (reserve_quantity >= 0),
        transit_quantity integer not null check (transit_quantity >= 0)
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists dc_products
    """)
    connection = op.get_bind()
    connection.execute(sql)

