# Validación distribuida con PySpark

Ejemplo para mostrar cómo PySpark facilita la validación y el preprocesamiento distribuido sobre el dataset real **“Ecommerce events history in cosmetics shop”**. Todo vive en un único notebook y se puede ejecutar tanto en modo local como sobre un clúster Spark con dos workers montado con Docker.

## Componentes del entorno

| Servicio | Rol | Puertos expuestos |
| --- | --- | --- |
| `spark-master` | Master de Spark (`spark://spark-master:7077`) basado en la misma imagen `jupyter/pyspark-notebook:spark-3.5.0` para compartir dependencias y versión de Python con el driver. | 7077 (RPC), 8080 (UI) |
| `spark-worker-1` / `spark-worker-2` | Workers (2 cores y 2 GB cada uno), también derivados de `jupyter/pyspark-notebook:spark-3.5.0` para evitar desajustes de Python. | 8081 / 8082 |
| `pyspark-notebook` | Imagen oficial `jupyter/pyspark-notebook:spark-3.5.0` limitada a 2 vCPU y 3 GB RAM para compararla contra un worker; instala automáticamente la extensión `jupyterlab_execute_time` para ver la duración de cada celda. | 8888 |

> Todos los contenedores comparten el directorio del repositorio en `/opt/project`, de modo que los workers pueden leer los mismos CSV que se referencian desde el notebook.

## Prerrequisitos de datos

El notebook asume la presencia del ZIP original en `PySpark/data/raw/ecommerce-events-history-in-cosmetics-shop.zip`. Si no está, descárgalo previamente con tu cuenta de Kaggle y colócalo en esa ruta. El propio notebook se encarga de descomprimirlo en `PySpark/data/bronze/` cuando sea necesario, por lo que los estudiantes solo tienen que ejecutar las celdas en orden.

Estructura esperada:

```
PySpark/data/
├── raw/
│   └── ecommerce-events-history-in-cosmetics-shop.zip
└── bronze/   # se rellena automáticamente
```

## Ejecución paso a paso

1. Levanta los servicios (master, dos workers y el notebook) desde esta carpeta:
   ```bash
   docker compose up -d spark-master spark-worker-1 spark-worker-2 pyspark-notebook
   ```
2. Abre `http://localhost:8888/?token=mlops` para entrar a JupyterLab. El notebook `pyspark_intro.ipynb` ya está en la raíz de `work/`.
3. Dentro del notebook:
   - **Parte A – Local**: crea una sesión `local[2]` para limitarse a los mismos recursos que un worker, realiza la ingesta, explora DataFrames vs. RDDs, ejecuta reglas de validación y entrena una regresión logística muy ligera midiendo tiempos de ejecución por celda.
   - **Parte B – Cluster**: cierra la sesión local, crea una nueva sesión apuntando a `spark://spark-master:7077` y ejecuta una agregación costosa para observar cómo se reparte el trabajo en múltiples particiones/ejecutores.
4. Si quieres visualizar el estado del cluster al correr la segunda parte, ingresa a:
   - UI del master: `http://localhost:8080`
   - UI worker 1: `http://localhost:8081`
   - UI worker 2: `http://localhost:8082`
5. Cuando termines, detén los servicios: `docker compose down`.

## Metodología de comparación

- El contenedor de Jupyter está limitado a **2 vCPU y 3 GB RAM** (equivalente a un worker) y la sesión local usa `local[2]`. Así observamos cómo escala el mismo flujo cuando se libera la restricción y se distribuye entre múltiples ejecutores.
- Los servicios `spark-master` y `spark-worker-*` usan la misma imagen base que el notebook y comparten `PYSPARK_PYTHON=/opt/conda/bin/python`, lo que evita errores de tipo *Python version mismatch* al enviar tareas al clúster.
- Se instaló automáticamente la extensión `jupyterlab_execute_time`, que muestra el tiempo de ejecución de cada celda en la interfaz. Además, las celdas críticas incluyen el magic `%%time` para registrar la duración en la propia salida.
- Durante la parte distribuida vuelve a ejecutar exactamente las mismas transformaciones para que puedas comparar los tiempos reportados entre ambos escenarios.

## Qué cubre el notebook

- Explicación breve del caso y ventajas de PySpark.
- Preparación automática de carpetas y descompresión del ZIP.
- Utilidades reutilizables para leer el dataset desde rutas compartidas (valen para local o cluster).
- Flujo completo de validación:
  - Perfilado de esquema y estadísticas.
  - Comparativa DataFrame vs. RDD.
  - Reglas educativas: precios no válidos, categorías faltantes y sesiones sospechosas.
  - Pipeline sencillo de `pyspark.ml` (VectorAssembler, StandardScaler, LogisticRegression).
- Los mismos pasos se repiten contra el clúster para comparar tiempos entre la sesión restringida (`local[2]`) y la ejecución distribuida.
- Reinicio del contexto y reconexión al master distribuido.
- Ejemplo de agregación y `explain()` para visualizar el DAG ejecutado en el cluster.

Con este material los estudiantes solo tienen que seguir el notebook y observar tanto la ejecución local como la distribuida, sin instalar nada adicional en su máquina anfitrión.
