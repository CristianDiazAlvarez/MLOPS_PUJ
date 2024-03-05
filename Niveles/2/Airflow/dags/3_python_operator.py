from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_hello():
    print("Hello MLOPS_PUJ")

with DAG(dag_id="3-pythonoperator",
         description="Utilizando Python Operator",
         schedule_interval="@once",
         start_date=datetime(2023,5,1)) as dag:
    
    t1 = PythonOperator(task_id= "hello_with_python",
                        python_callable=print_hello)