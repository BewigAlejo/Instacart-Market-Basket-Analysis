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

con.execute("""
    CREATE OR REPLACE VIEW aisles AS
    SELECT *
    FROM read_csv_auto('data/raw/aisles.csv')
""")

con.execute("""
    CREATE OR REPLACE VIEW departments AS
    SELECT *
    FROM read_csv_auto('data/raw/departments.csv')
""")

# Detalle enriquecido
con.execute("""
    CREATE OR REPLACE VIEW reorder_detail AS
    SELECT
        op.order_id,
        op.product_id,
        p.product_name,
        p.aisle_id,
        a.aisle,
        p.department_id,
        d.department,
        op.add_to_cart_order,
        op.reordered
    FROM order_products_prior op
    INNER JOIN products p
        ON op.product_id = p.product_id
    LEFT JOIN aisles a
        ON p.aisle_id = a.aisle_id
    LEFT JOIN departments d
        ON p.department_id = d.department_id
""")

# Métricas por producto
con.execute("""
    CREATE OR REPLACE VIEW product_reorder_metrics AS
    SELECT
        product_id,
        product_name,
        aisle,
        department,
        COUNT(*) AS total_purchases,
        SUM(reordered) AS reordered_purchases,
        ROUND(
            SUM(reordered) * 1.0 / COUNT(*),
            4
        ) AS reorder_rate
    FROM reorder_detail
    GROUP BY
        product_id,
        product_name,
        aisle,
        department
""")

print("\nTASA GLOBAL DE RECOMPRA")
con.sql("""
    SELECT
        COUNT(*) AS total_items,
        SUM(reordered) AS reordered_items,
        ROUND(
            SUM(reordered) * 1.0 / COUNT(*),
            4
        ) AS global_reorder_rate
    FROM order_products_prior
""").show()

print("\nPRODUCTOS CON MAYOR VOLUMEN DE RECOMPRA")
con.sql("""
    SELECT *
    FROM product_reorder_metrics
    ORDER BY reordered_purchases DESC
    LIMIT 20
""").show()

print("\nPRODUCTOS CON MAYOR TASA DE RECOMPRA")
print("(mínimo 1.000 compras para evitar productos con poco volumen)")

con.sql("""
    SELECT *
    FROM product_reorder_metrics
    WHERE total_purchases >= 1000
    ORDER BY reorder_rate DESC
    LIMIT 20
""").show()

print("\nRECOMPRA POR DEPARTAMENTO")
con.sql("""
    SELECT
        department,
        COUNT(*) AS total_purchases,
        SUM(reordered) AS reordered_purchases,
        ROUND(
            SUM(reordered) * 1.0 / COUNT(*),
            4
        ) AS reorder_rate
    FROM reorder_detail
    GROUP BY department
    ORDER BY reorder_rate DESC
""").show()

print("\nRECOMPRA POR AISLE")
con.sql("""
    SELECT
        aisle,
        COUNT(*) AS total_purchases,
        SUM(reordered) AS reordered_purchases,
        ROUND(
            SUM(reordered) * 1.0 / COUNT(*),
            4
        ) AS reorder_rate
    FROM reorder_detail
    GROUP BY aisle
    ORDER BY reorder_rate DESC
    LIMIT 20
""").show()