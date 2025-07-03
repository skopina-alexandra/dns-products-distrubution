from utils.db import create_db_connection
from psycopg2.extras import execute_values, DictCursor
import logging


def insert_into_distribution_plan(plan_values, connection):
    with connection.cursor() as cursor:
        execute_values(
            cursor,
            "insert into distribution_plan (product_id, branch_id, shipment) values %s",
            [
                (plan["product_id"], plan["branch_id"], plan["shipment"])
                for plan in plan_values
            ],
            template="(%s, %s, %s)",
        )

    connection.commit()
    logging.info(f"В таблицу распределения добавлено {len(plan_values)} записей...")


def get_available_dc_stock_for_product(product, connection):
    with connection.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(
            f"""
            select
                coalesce(dc.stock_quantity - dc.reserve_quantity,0) as available_dc
            from dc_products as dc
            where dc.product_id = \'{product}\'
            """
        )
        available_dc = cursor.fetchone()["available_dc"]
        return available_dc


def distribute():
    connection = create_db_connection()

    with connection.cursor(cursor_factory=DictCursor) as cursor:
        logging.info("Получаем дефициты товаров...")
        cursor.execute(
            """
            with
              deficit_branches as (
                select
                    n.branch_id as branch_id,
                    n.product_id AS product_id,
                    n.needs as demand,
                    coalesce(bp.stock_quantity - bp.reserve_quantity, 0) as current_stock,
                    coalesce(bp.transit_quantity, 0) as in_transit,
                    s.priority as priority,
                    greatest(0, n.needs - (coalesce(bp.stock_quantity - bp.reserve_quantity, 0) - coalesce(bp.transit_quantity, 0))) as deficit
                from needs as n
                inner join stores as s on n.branch_id = s.branch_id
                left join branch_products as bp
                    on n.branch_id = bp.branch_id and n.product_id = bp.product_id
            )
            -- ранжирование магазинов по приоритету
            select branch_id, product_id, demand, current_stock, in_transit, priority, deficit,
                row_number() over (
                    partition by product_id
                    order by priority desc, deficit desc
                ) as priority_rank
            from deficit_branches
            where deficit > 0  -- Только магазины с дефицитом
        """
        )

        plan_chunk_size = 500
        product = None
        plan = []
        available_dc = 0

        rows = cursor.fetchmany(plan_chunk_size)

        logging.info("Начинаем рспределение товаров...")

        while rows:
            for row in rows:
                if product != row["product_id"]:
                    product = row["product_id"]
                    available_dc = get_available_dc_stock_for_product(
                        product, connection
                    )

                shipment = min(row["demand"], available_dc)
                available_dc -= shipment
                if shipment > 0:
                    plan.append(
                        {
                            "product_id": row["product_id"],
                            "branch_id": row["branch_id"],
                            "shipment": shipment,
                        }
                    )

                if len(plan) > plan_chunk_size:
                    insert_into_distribution_plan(plan, connection)
                    plan.clear()

            rows = cursor.fetchmany(plan_chunk_size)

        if len(plan) > 0:
            insert_into_distribution_plan(plan, connection)

        logging.info("Распределение товаров завершено")
