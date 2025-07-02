from sqlalchemy import text, create_engine
from dotenv import load_dotenv
from utils.db import get_database_url
from psycopg2.extras import execute_values

load_dotenv()

# engine = create_engine(get_database_url())


def insert_into_distribution_plan(plan_values):
    engine = create_engine(get_database_url())
    with engine.connect() as plan_connection:
        cursor = plan_connection.connection.cursor()
        execute_values(
            cursor,
            "INSERT INTO distribution_plan (product_id, branch_id, shipment) VALUES %s",
            [
                (plan["product_id"], plan["branch_id"], plan["shipment"])
                for plan in plan_values
            ],
            template="(%s, %s, %s)",
        )
        cursor.close()


def get_available_dc_stock_for_product(product):
    engine = create_engine(get_database_url())
    with engine.connect() as dc_connection:
        sql_get_available = text(
            """ 
            select 
                coalesce(dc.stock_quantity - dc.reserve_quantity,0) as available_dc
            from dc_products as dc
            where dc.product_id = :product_id
            """
        )
        available_dc = dc_connection.execute(
            sql_get_available, parameters={"product_id": product}
        ).scalar()
        return available_dc


def distribute():
    engine = create_engine(get_database_url())
    with engine.connect() as connection:
        sql_shortage = text(
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
        result = connection.execution_options(stream_results=True).execute(sql_shortage)

        # sql_distribution_plan = text(
        #     """
        #     insert into distribution_plan (product_id, branch_id, shipment)
        #     values(:product_id, :branch_id, :shipment)
        #     """
        # )

        product = None
        plan = []
        available_dc = 0

        plan_chunk_size = 500

        for row in result:
            if product != row.product_id:
                product = row.product_id
                available_dc = get_available_dc_stock_for_product(product)

            shipment = min(row.demand, available_dc)
            available_dc -= shipment
            if shipment > 0:
                plan.append(
                    {
                        "product_id": row.product_id,
                        "branch_id": row.branch_id,
                        "shipment": shipment,
                    }
                )
            if len(plan) > plan_chunk_size:
                insert_into_distribution_plan(plan)
                plan.clear()

        if len(plan) > 0:
            insert_into_distribution_plan(plan)
