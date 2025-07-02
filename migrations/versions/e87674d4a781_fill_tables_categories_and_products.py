"""fill tables categories and products

Revision ID: e87674d4a781
Revises: b276eae9043d
Create Date: 2025-07-02 04:58:06.830995

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text
import pandas as pd


# revision identifiers, used by Alembic.
revision: str = "e87674d4a781"
down_revision: Union[str, Sequence[str], None] = "b276eae9043d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    df = pd.read_csv(
        "https://media.githubusercontent.com/media/skopina-alexandra/dns-products-distrubution/refs/heads/main/data/products.csv",
        dtype=str,
        quotechar='"',
        encoding="cp1251",
        skipinitialspace=True,
    )
    df["Category_ID"] = df["Category_ID"].str.replace('"', "")
    df["Category_ID"] = df["Category_ID"].str.strip()
    df["Product_ID"] = df["Category_ID"].str.replace('"', "")
    df["Product_ID"] = df["Category_ID"].str.strip()

    category_ids = df["Category_ID"].unique().tolist()
    df_categories = pd.DataFrame(
        {
            "id": category_ids,
            "name": [f"Категория{i+1}" for i in range(len(category_ids))],
        }
    )

    data_categories = df_categories.to_dict("records")

    connection = op.get_bind()

    sql_query = text(
        """
        INSERT INTO categories (id, name)
        VALUES (:id, :name)
        """
    )

    connection.execute(sql_query, data_categories)

    df = df.drop_duplicates(
        subset=["Product_ID"],
        keep="first",
    )  # удаляем повторяющиеся product_id
    df = df.rename(columns={"Product_ID": "product_id", "Category_ID": "category_id"})
    data_products = df.to_dict("records")

    sql_query = text(
        """
        INSERT INTO products (product_id, category_id)
        VALUES (:product_id, :category_id)
        """
    )
    connection.execute(sql_query, data_products)


def downgrade() -> None:
    sql = text(
        """
        truncate products cascade;
        truncate categories cascade;
    """
    )
    connection = op.get_bind()
    connection.execute(
        sql,
    )
