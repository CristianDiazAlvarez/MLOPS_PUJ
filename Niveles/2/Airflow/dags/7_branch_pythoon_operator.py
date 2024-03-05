from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime, date

default_args = {
'start_date': datetime(2023, 4, 15),
'end_date': datetime(2023, 6, 1),
"depends_on_past": True
}

def _choose(**context):
    if context["logical_date"].date() < date(2023, 4, 23):
        return "finish_23_april"
    return "start_24_april"

with DAG(dag_id="7-branching",
    schedule_interval="@daily",
	default_args=default_args,
    max_active_runs=1
) as dag:

    branching = BranchPythonOperator(task_id="branch",
	                                 python_callable=_choose)

    finish_23 = BashOperator(task_id="finish_23_april",
	                         bash_command="echo 'Running {{ds}}'")

    start_24 = BashOperator(task_id="start_24_april",
	                        bash_command="echo 'Running {{ds}}'")

    branching >> [finish_23, start_24]
