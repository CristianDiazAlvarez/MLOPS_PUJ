from airflow import DAG
from airflow.operators.bash import BashOperator 
from datetime import datetime


with DAG (dag_id= "2-bashoperator",
          description="Utilizando bash operator",
          start_date=datetime (2023,5,1)) as dag:
        
    t1 = BashOperator(task_id="hello_with_bash",
                      bash_command="echo 'Hello MLOPS_PUJ'")
    t1