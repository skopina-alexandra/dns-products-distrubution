"""fill tables dc and dc_products

Revision ID: c413ad476157
Revises: e87674d4a781
Create Date: 2025-07-02 16:33:24.785737

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text
import pandas as pd


# revision identifiers, used by Alembic.
revision: str = "c413ad476157"
down_revision: Union[str, Sequence[str], None] = "e87674d4a781"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    df = pd.read_csv(
        "https://media.githubusercontent.com/media/skopina-alexandra/dns-products-distrubution/refs/heads/main/data/rc_products.csv",
        dtype=str,
        quotechar='"',
        skipinitialspace=True,
        encoding="cp1251",
    )
    df = df.rename(
        columns={
            "Товар": "product_id",
            "РЦ": "dc_id",
            "Остаток": "stock_quantity",
            "Резерв": "reserve_quantity",
            "Транзит": "transit_quantity",
        }
    )
    dc_ids = df["dc_id"].unique().tolist()
    df_dc = pd.DataFrame(
        {
            "id": dc_ids,
            "name": [f"РЦ{i+1}" for i in range(len(dc_ids))],
        }
    )

    data_dc = df_dc.to_dict("records")

    connection = op.get_bind()

    sql_query = text(
        """
        insert into distribution_centers (id, name)
        values (:id, :name)
        """
    )

    connection.execute(sql_query, data_dc)

    result = connection.execute(text("select product_id from products"))
    existing_ids = [row[0] for row in result]
    df = df.sample(len(existing_ids)).copy()
    df["product_id"] = existing_ids
    data_dc_products = df.to_dict("records")

    sql_query = text(
        """
        insert into dc_products (dc_id, product_id, stock_quantity, reserve_quantity, transit_quantity)
        values (:dc_id, :product_id, :stock_quantity, :reserve_quantity, :transit_quantity)
        on conflict do nothing
        """
    )

    connection.execute(sql_query, data_dc_products)


def downgrade() -> None:
    sql = text(
        """
        truncate distribution_centers cascade;
        truncate dc_products cascade;
    """
    )
    connection = op.get_bind()
    connection.execute(sql)
