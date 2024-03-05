from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

def print_hello():
    print("Hello MLOPS_PUJ")

with DAG (dag_id="4-dependencies",
          description="Creando dependecias entre tareas",
          schedule_interval="@once",
          start_date=datetime (2023,5,1)) as dag:
    
    t1 = PythonOperator (task_id="tarea1",
                         python_callable=print_hello)
    t2 = BashOperator (task_id="tarea2",
                       bash_command="echo 'tarea2")
    t3 = BashOperator (task_id="tarea3",
                       bash_command="echo 'tarea3'")
    t4 = BashOperator (task_id="tarea4",
                      bash_command="echo 'tarea4'")
    
    t1 >> t2 >> [t3,t4]
