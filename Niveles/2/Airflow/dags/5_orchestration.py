from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG(dag_id="5-orchestration",
         description= "Probando la orquestacion",
         schedule_interval="@daily",
         start_date=datetime (2023,5,1),
         end_date=datetime (2023, 6, 1)) as dag:
         # default_args={"depends_on_past": True},
         # max_active_runs=5) as dag:
    
    t1 = BashOperator (task_id="tarea1",
                       bash_command="sleep 2 && echo 'Tarea 1'")
    t2 = BashOperator (task_id="tarea2",
                       bash_command="sleep 2 && echo 'Tarea 2'")
    t3 = BashOperator (task_id="tarea3",
                       bash_command="sleep 2 && echo 'Tarea 3'")
    t4 = BashOperator (task_id="tarea4",
                       bash_command="sleep 2 && echo 'Tarea 4'")
    
    t1 >> t2 >> [t3,t4]
