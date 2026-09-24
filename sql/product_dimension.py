import duckdb

con = duckdb.connect()

# Tablas base
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

# Dimensión de productos
con.execute("""
    CREATE OR REPLACE VIEW dim_products AS
    SELECT
        p.product_id,
        p.product_name,
        p.aisle_id,
        a.aisle,
        p.department_id,
        d.department
    FROM products p
    LEFT JOIN aisles a
        ON p.aisle_id = a.aisle_id
    LEFT JOIN departments d
        ON p.department_id = d.department_id
""")

print("\nDIMENSIÓN DE PRODUCTOS")
con.sql("""
    SELECT *
    FROM dim_products
    LIMIT 10
""").show()

print("\nCANTIDAD DE PRODUCTOS POR DEPARTAMENTO")
con.sql("""
    SELECT
        department,
        COUNT(*) AS total_products
    FROM dim_products
    GROUP BY department
    ORDER BY total_products DESC
""").show()