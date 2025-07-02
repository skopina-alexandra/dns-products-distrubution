"""create distribution_plan table

Revision ID: eef515e421e0
Revises: cb55635657df
Create Date: 2025-07-03 00:23:17.252112

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "eef515e421e0"
down_revision: Union[str, Sequence[str], None] = "cb55635657df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text(
        """
    create table distribution_plan(
        branch_id uuid not null references stores(branch_id) on delete cascade,
        product_id uuid not null references products(product_id) on delete cascade,
        shipment integer not null check(shipment >= 0)
    )
    """
    )
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text(
        """
    drop table if exists distribution_plan
    """
    )
    connection = op.get_bind()
    connection.execute(sql)
