Para traer configuracion de contenedor base de airflow

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.0/docker-compose.yaml'
```

En linux es necesario establecer la siguiente variable para la ejecucion, adicionalmente crear carpetar para establecer volumenes del contenedor.

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Para levantar airflow, con la configuracion por defecto.

```bash
docker compose up airflow-init
docker-compose up
```


Si no desea cargar los ejemplos cambie la siguiente variable a `false`

```
AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
```

Explore los ejemplos basicos expuestos en este repositorio.
Para continuar con la exploracion de airflow, se propone crear un workflow. Para esto debe definir primero la arquitectura que dara soporte a su experimentacion. Cree un primer contenedor que contenga una base de datos a la cual desea ingresar informacion. Un segundo contenedor, que aloje archivos planos con la informacion origen. En el contenedor de airflow, cree los DAGs necesarios para consumir periodicamente los archivos de texto plano y realice procesamiento que considere necesario para llevarlos a la base de datos creada.