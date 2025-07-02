"""fill table logdays

Revision ID: a7e8134b48e0
Revises: f1605ea3f875
Create Date: 2025-07-02 20:34:28.246483

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "a7e8134b48e0"
down_revision: Union[str, Sequence[str], None] = "f1605ea3f875"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = text(
        """
        insert into logdays (category_id, branch_id, logdays)
        select categories.id as category_id, 
            stores.branch_id as branch_id,
            7 as logdays
        from categories
        cross join stores
    """
    )
    connection = op.get_bind()
    connection.execute(sql)


def downgrade() -> None:
    sql = text(
        """
        truncate logdays cascade;           
    """
    )
    connection = op.get_bind()
    connection.execute(sql)
