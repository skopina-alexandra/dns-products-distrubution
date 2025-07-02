"""fill tables stores and branch_products

Revision ID: f1605ea3f875
Revises: c413ad476157
Create Date: 2025-07-02 18:00:16.741405

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text
import pandas as pd
import random
import numpy as np

# revision identifiers, used by Alembic.
revision: str = "f1605ea3f875"
down_revision: Union[str, Sequence[str], None] = "c413ad476157"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def assign_products_to_branch(branch_group, products):
    return pd.Series(products[: len(branch_group)], index=branch_group.index)


def limit_group_size(branch_group, max_size):
    return branch_group.sample(min(len(branch_group), max_size))


def upgrade() -> None:

    df = pd.read_csv(
        "https://media.githubusercontent.com/media/skopina-alexandra/dns-products-distrubution/refs/heads/main/data/branch_products.csv",
        dtype=str,
        quotechar='"',
        skipinitialspace=True,
        encoding="cp1251",
    )
    df = df.rename(
        columns={
            "Товар": "product_id",
            "Фирма": "branch_id",
            "Остаток": "stock_quantity",
            "Резерв": "reserve_quantity",
            "Транзит": "transit_quantity",
        }
    )

    branch_ids = df["branch_id"].unique().tolist()
    df_branch = pd.DataFrame(
        {
            "branch_id": branch_ids,
            "priority": [random.randint(1, 10) for i in range(len(branch_ids))],
        }
    )
    data_branches = df_branch.to_dict("records")

    connection = op.get_bind()

    sql_query = text(
        """
        insert into stores (branch_id, priority)
        values (:branch_id, :priority)
        """
    )

    connection.execute(sql_query, data_branches)

    result = connection.execute(text("select product_id from products"))
    existing_products = [row[0] for row in result]
    df = df.groupby("branch_id", group_keys=False).apply(
        lambda group: limit_group_size(group, len(existing_products))
    )
    df["product_id"] = df.groupby("branch_id", group_keys=False).apply(
        lambda group: assign_products_to_branch(group, existing_products)
    )

    data_branch_products = df.to_dict("records")
    sql_query = text(
        """
        insert into branch_products (branch_id, product_id, stock_quantity, reserve_quantity, transit_quantity)
        values (:branch_id, :product_id, :stock_quantity, :reserve_quantity, :transit_quantity)
        on conflict do nothing
        """
    )

    connection.execute(sql_query, data_branch_products)


def downgrade() -> None:
    sql = text(
        """
        truncate stores cascade;
        truncate branch_products cascade;
    """
    )
    connection = op.get_bind()
    connection.execute(sql)
