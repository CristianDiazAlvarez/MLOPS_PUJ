from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime, date

default_args = {
'start_date': datetime(2023, 5, 1),
'end_date': datetime(2023, 6, 1)
}

def _choose(**context):
    if context["logical_date"].date() < date(2023, 5, 8):
        return "finish_8_may"
    return "start_9_may"

with DAG(dag_id="7-branching",
    schedule_interval="@daily",
	default_args=default_args
) as dag:

    branching = BranchPythonOperator(task_id="branch",
	                                 python_callable=_choose)

    finish_8 = BashOperator(task_id="finish_8_may",
	                         bash_command="echo 'Running {{ds}}'")

    start_9 = BashOperator(task_id="start_9_may",
	                        bash_command="echo 'Running {{ds}}'")

    branching >> [finish_8, start_9]