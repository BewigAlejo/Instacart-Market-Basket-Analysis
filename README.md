# Instacart Market Basket Analysis

## Sobre el proyecto

Este proyecto de **Data Analytics** estudia el comportamiento de compra en Instacart mediante SQL, Python/pandas y Power BI. El objetivo es comprender qué compran los usuarios, cómo se componen sus canastas y qué patrones de recompra aparecen, para convertir los datos en hallazgos y recomendaciones de negocio.

La pregunta de negocio que orienta el proyecto es:

> ¿Qué productos y categorías conviene priorizar en acciones de recompra y venta cruzada, según su frecuencia de compra y su presencia conjunta en las canastas?

El foco está en dominar la preparación, el análisis y la comunicación de resultados. **El alcance no incluye modelos predictivos ni Machine Learning**, aunque los archivos originales utilicen los nombres `train` y `test`.

### Recorrido del proyecto

1. **Dataset real:** comprender qué representa, quién genera los datos y cuáles son sus limitaciones.
2. **Pregunta de negocio:** definir una pregunta útil para orientar decisiones comerciales.
3. **SQL y limpieza:** auditar la calidad, documentar problemas, limpiar cuando corresponda, unir tablas y validar los resultados.
4. **Análisis:** explorar con SQL y pandas, definir KPIs y crear variables útiles, diferenciando los hallazgos comprobados de las hipótesis.
5. **Dashboard:** construir una vista simple en Power BI que permita comparar productos, categorías y patrones de compra para apoyar una decisión.
6. **Recomendación:** elaborar un memo con 3–5 conclusiones accionables, sus riesgos y los próximos pasos.

### Stack y entregables

| Tecnología | Uso en el proyecto |
| --- | --- |
| **SQL** | Extracción, joins, agregaciones, CTEs, funciones de ventana, validaciones y construcción de tablas analíticas. |
| **Python + pandas** | Trabajo transversal: carga y combinación de datos, profiling, limpieza, tratamiento de nulos y duplicados, creación de variables, EDA y preparación de datasets para BI. |
| **Power BI** | Tecnología principal a incorporar: Power Query, modelo estrella, relaciones, DAX básico, KPIs, filtros y diseño con una narrativa ejecutiva. |
| **Git / GitHub** | Versionado del README, queries, notebooks, capturas del dashboard y memo de recomendaciones. |

**Estado actual:** la carga y auditoría inicial con pandas están documentadas en [01_data_profiling.ipynb](notebooks/01_data_profiling.ipynb). La exploración SQL comenzó con el catálogo de productos en [sql/product_dimension.py](sql/product_dimension.py). Los demás análisis SQL, el EDA, el dashboard y las recomendaciones continúan pendientes.

## Dataset y alcance del análisis

El **Instacart Market Basket Public Dataset** reúne registros anonimizados de pedidos generados por la actividad de compra de usuarios de Instacart. El repositorio utiliza la [copia disponible en Kaggle publicada por psparks](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis), que también descarga el script [instacart.py](instacart.py).

Las seis tablas cargadas en el notebook son:

| Tabla | Qué representa | Filas auditadas |
| --- | --- | ---: |
| `aisles` | Catálogo de pasillos o categorías intermedias. | 134 |
| `departments` | Catálogo de departamentos. | 21 |
| `products` | Productos y su clasificación por pasillo y departamento. | 49.688 |
| `orders` | Pedidos, usuario, secuencia de compra y variables temporales. | 3.421.083 |
| `order_products__prior` | Productos incluidos en los pedidos históricos. | 32.434.489 |
| `order_products__train` | Productos de los pedidos del subconjunto `train`. | 1.384.617 |

Cada fila de las tablas `order_products` representa **un producto dentro de un pedido**, no una cantidad de unidades físicas. Las relaciones se construyen mediante `order_id`, `product_id`, `aisle_id` y `department_id`.

### Limitaciones

- Las tablas analizadas no incluyen precios, costos ni márgenes: permiten medir frecuencia, composición de canastas y recompra, pero no ingresos ni rentabilidad.
- La información temporal contiene secuencia de pedidos, día codificado, hora e intervalo entre compras; no incluye fechas completas para estudiar estacionalidad por mes o año.
- Existen productos clasificados como `missing`; su presencia debe considerarse al comparar departamentos.


## Obtención de los datos

Los datos originales **no se almacenan directamente en este repositorio**. Se pueden descargar desde [Kaggle](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis) utilizando la biblioteca de Python `kagglehub`, sin subir los CSV a GitHub.

### 1. Instalar las bibliotecas necesarias

```bash
pip install kagglehub pandas
```

### 2. Autenticarse en Kaggle

Si tu entorno requiere autenticación:

```python
import kagglehub

kagglehub.login()
```

Podés generar las credenciales de la API desde la configuración de tu cuenta de Kaggle.

> Nunca subas tu token de Kaggle, `kaggle.json` ni archivos `.env` a GitHub.

### 3. Descargar el dataset

```python
import kagglehub

path = kagglehub.dataset_download(
    "psparks/instacart-market-basket-analysis"
)

print("Ruta del dataset:", path)
```

`kagglehub` guarda el dataset en su caché local y devuelve la ruta de la carpeta descargada. El script [instacart.py](instacart.py) realiza esta misma descarga.

### 4. Inspeccionar los archivos descargados

```python
import os

files = os.listdir(path)

for file in files:
    print(file)
```

Los archivos utilizados en el proyecto son:

```text
aisles.csv
departments.csv
products.csv
orders.csv
order_products__prior.csv
order_products__train.csv
```

### 5. Cargar una tabla con pandas

Por ejemplo, la tabla de pedidos se puede cargar directamente desde la caché:

```python
import pandas as pd
import os

orders = pd.read_csv(
    os.path.join(path, "orders.csv")
)

orders.head()
```

A partir de este punto, los datos están listos para la etapa de **profiling y evaluación de calidad**.

### Ejecutar el notebook del repositorio

El ejemplo anterior lee desde la caché. El notebook [01_data_profiling.ipynb](notebooks/01_data_profiling.ipynb) utiliza `../data/raw`: para ejecutarlo tal como está, copiá los seis CSV de la carpeta indicada por `path` a `data/raw`, conservando sus nombres y sin carpetas intermedias. Esa carpeta está excluida de Git mediante `.gitignore`.

Desde la raíz del repositorio, instalá JupyterLab y abrilo en la carpeta de notebooks:

```bash
pip install jupyterlab
cd notebooks
python -m jupyterlab
```

Abrí `01_data_profiling.ipynb` y ejecutá las celdas en orden. La tabla histórica supera los 32 millones de filas, por lo que la auditoría puede requerir varios GB de RAM y algunos minutos de procesamiento.

## Calidad de datos y auditoría

La auditoría de [01_data_profiling.ipynb](notebooks/01_data_profiling.ipynb) revisó estructura, tipos, valores faltantes, duplicados, claves y dominios, además de las relaciones entre tablas. Las decisiones se tomaron según el significado de los datos: un valor inusual no se corrigió automáticamente.

### `aisles`

Se revisaron los 134 pasillos. No se encontraron nulos ni filas duplicadas; tanto `aisle_id` como los nombres son únicos, y los identificadores van de 1 a 134. Los tipos son adecuados y **no se realizaron transformaciones ni limpieza correctiva**.

### `departments`

Los 21 departamentos tienen identificadores y nombres únicos, sin nulos ni duplicados. Se identificó el departamento `missing` (`department_id = 21`), que es una categoría explícita y no un `NaN`. **Se conservó sin cambios**, junto con el resto del catálogo.

### `order_products__prior`

Se auditaron 32.434.489 líneas de producto correspondientes a 3.214.874 pedidos. No hay nulos, filas duplicadas ni repeticiones en `(order_id, product_id)` o `(order_id, add_to_cart_order)`. Todos los pedidos y productos referenciados existen en sus tablas principales.

`reordered` solo contiene 0 y 1; el 58,97 % de las líneas está marcado como recompra. Las posiciones de carrito van de 1 a 145. Se conservaron los pedidos grandes, ya que su tamaño no demuestra un error. Hay 11 productos del catálogo que no aparecen en este subconjunto, lo que tampoco implica por sí solo un problema. **No se aplicó limpieza correctiva**.

### `order_products__train`

Se revisaron 1.384.617 líneas de producto de 131.209 pedidos, sin nulos, duplicados completos ni duplicaciones lógicas de producto o posición dentro del pedido. La auditoría documenta integridad referencial con `orders` y `products`, y correspondencia con `eval_set = 'train'`.

Las posiciones del carrito van de 1 a 80 y `reordered` mantiene su dominio binario; el 59,86 % de las líneas corresponde a recompra. **Se conservaron los registros y tipos originales**, sin imputaciones ni eliminaciones.

### `orders`

La tabla contiene 3.421.083 pedidos de 206.209 usuarios, sin filas duplicadas y con `order_id` único. Se validaron los rangos de día (0–6), hora (0–23) e intervalo registrado entre pedidos (0–30 días).

Los únicos nulos son los 206.209 valores de `days_since_prior_order` asociados al primer pedido de cada usuario, aproximadamente el 6,03 % de las filas. Son faltantes esperados porque no existe un pedido anterior: **no se imputaron ni se eliminaron**. Se mantuvo esta columna como `float64` y los códigos de día y hora como enteros, sin convertirlos en fechas completas.

### `products`

Los 49.688 productos tienen identificadores y nombres únicos, sin nulos ni filas duplicadas. Los identificadores son positivos y todas las referencias a pasillos y departamentos existen en sus catálogos.

Se encontraron 1.258 productos asociados simultáneamente al departamento `missing` (21) y al pasillo `missing` (100). Sus identificadores y nombres son válidos: **se conservaron como una categoría propia, sin eliminar ni imputar su clasificación**. Esta limitación se tendrá en cuenta en los análisis posteriores por categoría.

### Resultado de esta etapa

Los controles documentados no justifican limpieza correctiva. Se preservaron los nulos estructurales, las categorías `missing` y los registros válidos de tamaño inusual. Las tasas de recompra observadas son descripciones iniciales de líneas de producto, no conclusiones sobre la proporción de usuarios recurrentes ni sobre el impacto de una acción comercial.

## Análisis SQL

La carpeta [sql](sql/) organiza las consultas por tema de negocio. Actualmente utiliza archivos Python para ejecutar SQL con **DuckDB**, que permite consultar archivos CSV sin configurar un servidor de base de datos.

### Organización de la carpeta

| Archivo | Propósito | Estado |
| --- | --- | --- |
| [product_dimension.py](sql/product_dimension.py) | Explorar el tamaño del catálogo y su distribución por departamento y pasillo. | Implementado. |
| [reorder_analysis.py](sql/reorder_analysis.py) | Análisis previsto de recompra de productos y categorías. | Pendiente; archivo vacío. |
| [customer_behavior.py](sql/customer_behavior.py) | Análisis previsto del comportamiento de compra de los usuarios. | Pendiente; archivo vacío. |
| [temporal_analysis.py](sql/temporal_analysis.py) | Análisis previsto de patrones temporales de los pedidos. | Pendiente; archivo vacío. |
| [cross_sell.py](sql/cross_sell.py) | Análisis previsto de productos comprados juntos y oportunidades de venta cruzada. | Pendiente; archivo vacío. |

### Exploración del catálogo de productos

`product_dimension.py` lee `data/processed/dim_products.csv` y crea una vista temporal de consulta llamada `dim_products`. Sobre ella ejecuta tres consultas:

- **Cantidad total de productos:** cuenta las filas de la dimensión con `COUNT(*)`.
- **Productos por departamento:** agrupa por `department` y ordena los departamentos de mayor a menor cantidad de productos.
- **Productos por pasillo:** agrupa por `aisle` y muestra los 20 pasillos con más productos en el catálogo.

Estas consultas describen la composición del catálogo. Sus conteos no representan ventas, unidades compradas ni tasas de recompra. Los resultados se muestran en la terminal; el script no modifica los CSV ni exporta tablas nuevas.

### Cómo ejecutar las consultas

El script requiere que exista `data/processed/dim_products.csv`, con una fila por producto y las columnas descriptivas `department` y `aisle`. Este archivo procesado está excluido de Git y debe prepararse previamente a partir de `products`, `departments` y `aisles`; el script SQL no realiza esa preparación.

Desde la **raíz del repositorio**, instalá DuckDB y ejecutá:

```bash
pip install duckdb
python sql/product_dimension.py
```

Es importante ejecutar el comando desde la raíz porque la ruta `data/processed/dim_products.csv` se resuelve respecto del directorio de trabajo. Los restantes scripts se completarán a medida que avance el análisis.
