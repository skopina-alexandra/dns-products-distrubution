"""fill table needs

Revision ID: cb55635657df
Revises: a7e8134b48e0
Create Date: 2025-07-02 21:21:54.745717

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "cb55635657df"
down_revision: Union[str, Sequence[str], None] = "a7e8134b48e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text(
        """
        insert into needs (branch_id, product_id, needs)
        with needs_data as (
            select 
                stores.branch_id as branch_id, 
                products.product_id as product_id,
                products.category_id as category_id,
                coalesce(branch_products.stock_quantity, 0) as stock,
                coalesce(logdays.logdays, 7) as logdays
            from stores
            cross join products
            left join branch_products on 
                branch_products.product_id = products.product_id 
                and 
                branch_products.branch_id=stores.branch_id
            left join logdays on 
                logdays.branch_id = stores.branch_id 
                and 
                logdays.category_id = products.category_id
        )

        select 
            needs_data.branch_id as branch_id, 
            needs_data.product_id as product_id,
            floor(1 + random() * (greatest(150, needs_data.stock) * needs_data.logdays))::integer as needs
        from needs_data
    """
    )
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text(
        """
        truncate needs cascade;           
    """
    )
    connection = op.get_bind()
    connection.execute(sql)
