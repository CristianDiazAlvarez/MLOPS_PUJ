from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _print_message() -> None:
    print("Airflow en Kubernetes local: DAG de ejemplo ejecutado.")


with DAG(
    dag_id="hello_level3",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["nivel3", "kubernetes", "mlops"],
) as dag:
    say_hello = PythonOperator(
        task_id="say_hello",
        python_callable=_print_message,
    )

    say_hello
