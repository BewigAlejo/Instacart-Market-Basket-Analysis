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

con.execute("""
    CREATE OR REPLACE VIEW basket_summary AS
    SELECT
        order_id,
        COUNT(*) AS basket_size,
        SUM(reordered) AS reordered_items
    FROM order_products_prior
    GROUP BY order_id
""")

con.execute("""
    CREATE OR REPLACE VIEW temporal_orders AS
    SELECT
        o.order_id,
        o.user_id,
        o.order_number,
        o.order_dow,
        o.order_hour_of_day,
        o.days_since_prior_order,
        b.basket_size,
        b.reordered_items,

        b.reordered_items * 1.0
        / NULLIF(b.basket_size, 0) AS reorder_rate

    FROM orders o

    INNER JOIN basket_summary b
        ON o.order_id = b.order_id

    WHERE o.eval_set = 'prior'
""")

print("\nPEDIDOS POR DÍA DE LA SEMANA")

con.sql("""
    SELECT
        order_dow,
        COUNT(*) AS total_orders,
        ROUND(AVG(basket_size), 2) AS avg_basket_size,
        ROUND(AVG(reorder_rate), 4) AS avg_reorder_rate
    FROM temporal_orders
    GROUP BY order_dow
    ORDER BY order_dow
""").show()

print("\nPEDIDOS POR HORA")

con.sql("""
    SELECT
        order_hour_of_day,
        COUNT(*) AS total_orders,
        ROUND(AVG(basket_size), 2) AS avg_basket_size,
        ROUND(AVG(reorder_rate), 4) AS avg_reorder_rate
    FROM temporal_orders
    GROUP BY order_hour_of_day
    ORDER BY order_hour_of_day
""").show()

print("\nDÍAS ENTRE PEDIDOS")

con.sql("""
    SELECT
        days_since_prior_order,
        COUNT(*) AS total_orders,
        ROUND(AVG(reorder_rate), 4) AS avg_reorder_rate
    FROM temporal_orders
    WHERE days_since_prior_order IS NOT NULL
    GROUP BY days_since_prior_order
    ORDER BY days_since_prior_order
""").show()