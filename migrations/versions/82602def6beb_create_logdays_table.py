"""create logdays table

Revision ID: 82602def6beb
Revises: 12410489a753
Create Date: 2025-07-02 00:29:34.614744

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '82602def6beb'
down_revision: Union[str, Sequence[str], None] = '12410489a753'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""create logdays table

Revision ID: 82602def6beb
Revises: 12410489a753
Create Date: 2025-07-02 00:29:34.614744

"""

def upgrade() -> None:
    sql = text("""
    create table logdays(
        branch_id uuid not null references stores(branch_id) on delete cascade,
        category_id uuid not null references categories(id) on delete cascade,
        logdays smallint not null check(logdays > 0)
    )
    """)
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text("""
    drop table if exists logdays
    """)
    connection = op.get_bind()
    connection.execute(sql)

