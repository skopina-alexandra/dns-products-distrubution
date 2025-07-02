"""create branch_products table

Revision ID: b276eae9043d
Revises: 260d1de87be5
Create Date: 2025-07-02 01:57:10.094667

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "b276eae9043d"
down_revision: Union[str, Sequence[str], None] = "260d1de87be5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text(
        """
    create table branch_products(
        branch_id uuid not null references stores(branch_id) on delete restrict,
        product_id uuid not null references products(product_id) on delete restrict,
        stock_quantity integer not null,
        reserve_quantity integer not null,
        transit_quantity integer not null
    )
    """
    )
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text(
        """
    drop table if exists branch_products
    """
    )
    connection = op.get_bind()
    connection.execute(sql)
