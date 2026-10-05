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

**Estado actual:** la carga y auditoría inicial con pandas están documentadas en [01_data_profiling.ipynb](notebooks/01_data_profiling.ipynb). Los cinco scripts de la carpeta [sql](sql/) ya implementan consultas con DuckDB sobre el catálogo, la recompra, los clientes, los patrones temporales y las compras conjuntas. El EDA está documentado y ejecutado en [02_eda.ipynb](notebooks/02_eda.ipynb), con KPIs, gráficos y métricas de asociaciones. El dashboard y la validación de las recomendaciones comerciales continúan pendientes.

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

## Análisis SQL con DuckDB

La carpeta [sql](sql/) contiene cinco scripts Python que ejecutan SQL con **DuckDB**. Cada archivo abre su propia conexión en memoria, lee los CSV de `data/raw` y construye vistas mediante joins y agregaciones. Se pueden ejecutar de forma independiente: no requieren un servidor de base de datos ni archivos previamente generados en `data/processed`.

### Catálogo de productos — `product_dimension.py`

Une `products` con `aisles` y `departments` mediante `LEFT JOIN` para crear `dim_products`, incorporando el nombre del pasillo y del departamento a cada producto. Muestra una muestra de la dimensión y cuenta los productos por departamento. Estos conteos describen la composición del catálogo, no el volumen de compras.

### Recompra — `reorder_analysis.py`

Enriquece `order_products__prior` con los nombres de productos, pasillos y departamentos. Calcula la tasa global de recompra, las compras y recompras por producto, y las tasas por departamento y pasillo. Presenta los 20 productos con más recompras y los 20 con mayor tasa, exigiendo al menos **1.000 compras** en este último ranking para evitar destacar productos con poco volumen. La tasa representa la proporción de líneas de producto marcadas como `reordered = 1`.

### Comportamiento de clientes — `customer_behavior.py`

Agrupa primero los productos históricos por pedido para obtener el tamaño de la canasta y la cantidad de productos recomprados. Luego une ese resumen con `orders` por `order_id`, conserva los pedidos `prior` y calcula por usuario: cantidad de pedidos, líneas de producto, tamaño medio de canasta, tasa de recompra e intervalo medio entre compras. Muestra los 20 usuarios con más pedidos y KPIs generales; los promedios generales de canasta y recompra se calculan sobre las métricas de cada usuario, dando el mismo peso a cada uno.

### Patrones temporales — `temporal_analysis.py`

Une el resumen de canastas históricas con `orders` para analizar únicamente pedidos `prior`. Compara cantidad de pedidos, tamaño medio de canasta y tasa media de recompra por día codificado (0–6) y hora (0–23). También agrupa por días desde el pedido anterior, excluyendo los nulos estructurales de ese cálculo. La recompra se promedia a nivel de pedido, por lo que no equivale necesariamente a la tasa global calculada sobre todas las líneas de producto.

### Compras conjuntas — `cross_sell.py`

Selecciona los **500 productos presentes en más pedidos históricos** y realiza un autojoin por `order_id` para encontrar pares comprados juntos. La condición `product_id_1 < product_id_2` evita emparejar un producto consigo mismo y contar ambas versiones del mismo par. Después incorpora los nombres y calcula cuántos pedidos comparten cada par y la confianza en ambas direcciones: qué proporción de los pedidos con un producto también contiene el otro.

Muestra hasta 30 pares por frecuencia conjunta y hasta 30 por confianza del producto 1 al 2, considerando solo pares presentes en **al menos 100 pedidos**. El análisis está limitado a esos 500 productos y permite explorar oportunidades de venta cruzada; la presencia conjunta no demuestra el efecto de una promoción.

### Cómo ejecutar los scripts

Con los CSV descargados en `data/raw`, ejecutá desde la **raíz del repositorio**:

```bash
pip install duckdb
python sql/product_dimension.py
python sql/reorder_analysis.py
python sql/customer_behavior.py
python sql/temporal_analysis.py
python sql/cross_sell.py
```

Cada comando muestra sus resultados en la terminal. Los scripts no modifican los CSV originales ni exportan nuevas tablas; las vistas existen durante la ejecución de cada proceso. Los análisis transaccionales utilizan `order_products__prior`, sin incorporar `order_products__train` ni pedidos de `test`.

## EDA — Análisis exploratorio de datos

El notebook [02_eda.ipynb](notebooks/02_eda.ipynb) utiliza **pandas, matplotlib y DuckDB** para explorar la recompra y las oportunidades de venta cruzada. Los resultados e interpretaciones están documentados junto a cada análisis.

### ¿Cuál es la escala y el comportamiento general?

Se calcularon usuarios, pedidos, catálogo, líneas compradas, recompra, tamaño de canasta e intervalo entre pedidos. Hay **206.209 usuarios**, **3.421.083 pedidos** y **49.688 productos**. El histórico `prior` contiene **32.434.489 líneas** en **3.214.874 pedidos**, con **58,97 % de recompra** y **10,09 productos por canasta**. El intervalo registrado promedio en `orders` es **11,11 días**, excluyendo los nulos del primer pedido.

Los conteos generales, intervalos y patrones temporales usan `orders` completo; las canastas, la recompra y las asociaciones usan solo `prior`. La recompra mide líneas de producto, no el porcentaje de usuarios recurrentes.

### ¿Cuándo se registran más pedidos?

Se agruparon pedidos por día codificado y hora. Los códigos **0 y 1 concentran 34,74 %** del total; el máximo horario ocurre a las **10 h**, con **288.418 pedidos**. Entre las **9 y las 17 h** se registra **71,61 %** del volumen. Estos patrones permiten explorar necesidades operativas, sin asignar días calendario ni inferir estacionalidad.

### ¿Qué productos tienen más compras y mayor recurrencia?

Se compararon los 15 productos con más compras y los 15 con mayor tasa de recompra, exigiendo **10.000 compras** para este último ranking. **Banana** lidera el volumen (**472.565 compras**), seguida por **Bag of Organic Bananas** (**379.450**). Por tasa destacan **Milk, Organic, Vitamin D (85,43 %)** y **Organic Reduced Fat Milk (85,07 %)**. Se distinguen así alcance y recurrencia para explorar acciones de reposición.

### ¿Qué departamentos y pasillos impulsan la recompra?

Se compararon tasas agregadas y volumen por categoría; en pasillos se exigieron **10.000 compras**. **dairy eggs (67,00 %)** lidera la tasa de departamentos, mientras **produce** concentra el mayor volumen (**9.479.291 compras**). En pasillos destacan **milk (78,14 %)**, **water seltzer sparkling water (72,96 %)** y **fresh fruits (71,81 %)**. Se preservó la clasificación `missing`.

### ¿Qué productos se compran juntos?

Con SQL en DuckDB se analizaron pares entre los **500 productos presentes en más pedidos históricos**, evitando pares repetidos y contando pedidos distintos. Se calcularon **soporte**, **confianza en ambas direcciones** y **lift**, conservando pares con **al menos 100 pedidos conjuntos**. Las métricas se exportan a `data/processed/cross_sell_metrics.csv` (**81.646 pares** en esta ejecución).

**Bag of Organic Bananas + Organic Hass Avocado** es el par más frecuente (**62.341 pedidos**, soporte **1,94 %**, lift **2,47**). Al ordenar por lift y exigir **1.000 pedidos conjuntos**, destacan combinaciones de yogures: el primer par alcanza **73,64** de lift, pero solo **0,22 %** de soporte. Una asociación fuerte puede tener poco alcance; por eso se interpretan las tres métricas juntas.

### Interpretación y próximos pasos

Los hallazgos permiten evaluar reposición de productos recurrentes y pruebas de recomendaciones basadas en pares. Son **asociaciones descriptivas**, sin evidencia de impacto causal ni rentabilidad. El análisis de pares excluye productos fuera del top 500; los intervalos registrados están limitados a 0–30 y no hay precios ni fechas completas. El siguiente paso es comunicar los KPIs en Power BI y validar las propuestas comerciales.

### Cómo reproducir el EDA

1. Descargar los CSV y colocarlos en `data/raw`.
2. Ejecutar la preparación de tablas de `notebooks/01_data_profiling.ipynb` para generar los cinco CSV de `data/processed`. Los scripts de `sql` no los exportan.
3. Instalar `pandas`, `matplotlib` y `duckdb` en el entorno del kernel. Desde Jupyter se puede usar `%pip install pandas matplotlib duckdb` y reiniciar el kernel.
4. Abrir `notebooks/02_eda.ipynb` y ejecutar **Restart Kernel and Run All**. Las rutas admiten iniciar Jupyter desde la raíz del repositorio o desde `notebooks`.
