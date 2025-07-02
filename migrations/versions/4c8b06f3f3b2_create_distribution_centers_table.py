"""create distribution_centers table

Revision ID: 4c8b06f3f3b2
Revises: 82602def6beb
Create Date: 2025-07-02 01:25:22.348125

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '4c8b06f3f3b2'
down_revision: Union[str, Sequence[str], None] = '82602def6beb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text("""
    create table distribution_centers(
        id uuid primary key,
        name varchar(50) not null
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists distribution_centers
    """)
    connection = op.get_bind()
    connection.execute(sql)

