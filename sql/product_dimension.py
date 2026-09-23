import duckdb

duckdb.sql("""
    CREATE VIEW dim_products AS
    SELECT *
    FROM read_csv_auto('data/processed/dim_products.csv')
""")

print("Cantidad total de productos:")
duckdb.sql("""
    SELECT COUNT(*) AS total_products
    FROM dim_products
""").show()

print("Productos por departamento:")
duckdb.sql("""
    SELECT
        department,
        COUNT(*) AS total_products
    FROM dim_products
    GROUP BY department
    ORDER BY total_products DESC
""").show()

print("Productos por aisle:")
duckdb.sql("""
    SELECT
        aisle,
        COUNT(*) AS total_products
    FROM dim_products
    GROUP BY aisle
    ORDER BY total_products DESC
    LIMIT 20
""").show()

