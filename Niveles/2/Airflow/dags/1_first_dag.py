from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator

with DAG(dag_id="1-miprimerdag",
         description='primer dag',
         start_date=datetime(2023,5,1),
         schedule_interval="@once") as dag:
    t1 = EmptyOperator(task_id="dummy")
    
    t1