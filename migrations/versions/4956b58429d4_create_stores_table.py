"""create stores table

Revision ID: 4956b58429d4
Revises: 92149679b7d7
Create Date: 2025-07-02 00:01:34.201860

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '4956b58429d4'
down_revision: Union[str, Sequence[str], None] = '92149679b7d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text("""
    create table stores(
        branch_id uuid primary key,
        priority smallint not null check(priority > 0)
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists stores
    """)
    connection = op.get_bind()
    connection.execute(sql)
