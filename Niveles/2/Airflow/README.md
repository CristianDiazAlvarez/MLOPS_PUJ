
## Airflow

Para traer configuración de contenedor base de airflow

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.0/docker-compose.yaml'
```

En Linux es necesario establecer la siguiente variable para la ejecución, adicionalmente crear carpeta para establecer volúmenes del contenedor.

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Para levantar airflow, con la configuración por defecto.

```bash
docker compose up airflow-init
docker-compose up
```


Si no desea cargar los ejemplos cambie la siguiente variable a `false`

```
AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
```

Explore los ejemplos básicos expuestos en este repositorio.
Para continuar con la exploración de airflow, se propone crear un workflow. Para esto debe definir primero la arquitectura que dará soporte a su experimentación. Cree un primer contenedor que contenga una base de datos a la cual desea ingresar información. Un segundo contenedor, que aloje archivos planos con la información origen. En el contenedor de airflow, cree los DAGs necesarios para consumir periódicamente los archivos de texto plano y realice procesamiento que considere necesario para llevarlos a la base de datos creada.

## Taller Airflow

Usando docker compose:

1. Cree una instancia de una base de datos de preferencia (sugerencia: mysql)
	- Esta base de datos debe ser exclusiva para datos, los metadatos de airflow deben estar en una diferente.

2. Cree una instancia de Airflow.

3. Cree un DAG (con multiples tareas) que le permitan:
	- Borrar contenido base de datos
    - Cargar datos de penguins a la base de datos, sin preprocesamiento!
	- Realizar preprocesamiento para entrenamiento de modelo
	- Realizar entrenamiento de modelo usando datos preprocesados de la base de datos 
4. Cree API que permita realizar inferencia al modelo entrenado

Todos los servicios deben existir en el mismo docker compose!
