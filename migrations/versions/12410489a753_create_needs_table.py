"""create needs table

Revision ID: 12410489a753
Revises: 4956b58429d4
Create Date: 2025-07-02 00:19:16.954493

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '12410489a753'
down_revision: Union[str, Sequence[str], None] = '4956b58429d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text("""
    create table needs(
        branch_id uuid not null references stores(branch_id) on delete cascade,
        product_id uuid not null references products(product_id) on delete cascade,
        needs smallint not null check(needs >= 0)
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists needs
    """)
    connection = op.get_bind()
    connection.execute(sql)
