import duckdb

con = duckdb.connect()

con.execute("""
    CREATE OR REPLACE VIEW order_products_prior AS
    SELECT *
    FROM read_csv_auto('data/raw/order_products__prior.csv')
""")

con.execute("""
    CREATE OR REPLACE VIEW products AS
    SELECT *
    FROM read_csv_auto('data/raw/products.csv')
""")

# Productos con mayor presencia en pedidos
con.execute("""
    CREATE OR REPLACE VIEW top_products AS
    SELECT
        product_id,
        COUNT(DISTINCT order_id) AS product_orders
    FROM order_products_prior
    GROUP BY product_id
    ORDER BY product_orders DESC
    LIMIT 500
""")

# Filtrar líneas solo a esos productos
con.execute("""
    CREATE OR REPLACE VIEW basket_top_products AS
    SELECT
        op.order_id,
        op.product_id
    FROM order_products_prior op
    INNER JOIN top_products tp
        ON op.product_id = tp.product_id
""")

# Pares de productos dentro del mismo pedido
con.execute("""
    CREATE OR REPLACE VIEW product_pairs AS
    SELECT
        a.product_id AS product_id_1,
        b.product_id AS product_id_2,
        COUNT(DISTINCT a.order_id) AS orders_together
    FROM basket_top_products a

    INNER JOIN basket_top_products b
        ON a.order_id = b.order_id
       AND a.product_id < b.product_id

    GROUP BY
        a.product_id,
        b.product_id
""")

# Agregar nombres y calcular métricas
con.execute("""
    CREATE OR REPLACE VIEW cross_sell_metrics AS
    SELECT
        pp.product_id_1,
        p1.product_name AS product_1,

        pp.product_id_2,
        p2.product_name AS product_2,

        pp.orders_together,

        tp1.product_orders AS orders_product_1,
        tp2.product_orders AS orders_product_2,

        ROUND(
            pp.orders_together * 1.0
            / tp1.product_orders,
            4
        ) AS confidence_1_to_2,

        ROUND(
            pp.orders_together * 1.0
            / tp2.product_orders,
            4
        ) AS confidence_2_to_1

    FROM product_pairs pp

    INNER JOIN products p1
        ON pp.product_id_1 = p1.product_id

    INNER JOIN products p2
        ON pp.product_id_2 = p2.product_id

    INNER JOIN top_products tp1
        ON pp.product_id_1 = tp1.product_id

    INNER JOIN top_products tp2
        ON pp.product_id_2 = tp2.product_id
""")

print("\nPRINCIPALES PARES DE PRODUCTOS")

con.sql("""
    SELECT *
    FROM cross_sell_metrics
    WHERE orders_together >= 100
    ORDER BY orders_together DESC
    LIMIT 30
""").show()

print("\nPARES CON MAYOR CONFIANZA 1 -> 2")

con.sql("""
    SELECT *
    FROM cross_sell_metrics
    WHERE orders_together >= 100
    ORDER BY confidence_1_to_2 DESC
    LIMIT 30
""").show()