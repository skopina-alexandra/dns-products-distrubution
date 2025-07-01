"""create_category_table

Revision ID: 66ff6c3759df
Revises: 
Create Date: 2025-07-01 13:16:48.078617

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '66ff6c3759df'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text("""
    create table categories(
        id uuid primary key,
        name varchar(50) not null
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists categories
    """)
    connection = op.get_bind()
    connection.execute(sql)
