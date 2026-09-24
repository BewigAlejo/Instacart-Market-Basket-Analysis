import duckdb

con = duckdb.connect()

con.execute("""
    CREATE OR REPLACE VIEW orders AS
    SELECT *
    FROM read_csv_auto('data/raw/orders.csv')
""")

con.execute("""
    CREATE OR REPLACE VIEW order_products_prior AS
    SELECT *
    FROM read_csv_auto('data/raw/order_products__prior.csv')
""")

# Resumen de cada pedido
con.execute("""
    CREATE OR REPLACE VIEW basket_summary AS
    SELECT
        order_id,
        COUNT(*) AS basket_size,
        SUM(reordered) AS reordered_items
    FROM order_products_prior
    GROUP BY order_id
""")

# Comportamiento por usuario
con.execute("""
    CREATE OR REPLACE VIEW customer_behavior AS
    SELECT
        o.user_id,

        COUNT(DISTINCT o.order_id) AS total_prior_orders,

        SUM(b.basket_size) AS total_items,

        ROUND(
            AVG(b.basket_size),
            2
        ) AS avg_basket_size,

        SUM(b.reordered_items) AS reordered_items,

        ROUND(
            SUM(b.reordered_items) * 1.0
            / NULLIF(SUM(b.basket_size), 0),
            4
        ) AS reorder_rate,

        ROUND(
            AVG(o.days_since_prior_order),
            2
        ) AS avg_days_between_orders

    FROM orders o

    INNER JOIN basket_summary b
        ON o.order_id = b.order_id

    WHERE o.eval_set = 'prior'

    GROUP BY o.user_id
""")

print("\nRESUMEN DE COMPORTAMIENTO DE CLIENTES")

con.sql("""
    SELECT *
    FROM customer_behavior
    ORDER BY total_prior_orders DESC
    LIMIT 20
""").show()

print("\nKPIs GENERALES DE CLIENTES")

con.sql("""
    SELECT
        COUNT(*) AS total_users,

        ROUND(
            AVG(total_prior_orders),
            2
        ) AS avg_orders_per_user,

        ROUND(
            AVG(avg_basket_size),
            2
        ) AS avg_basket_size,

        ROUND(
            AVG(reorder_rate),
            4
        ) AS avg_user_reorder_rate,

        ROUND(
            AVG(avg_days_between_orders),
            2
        ) AS avg_days_between_orders

    FROM customer_behavior
""").show()