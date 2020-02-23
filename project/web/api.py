from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

DAGS_DIR = "/home/vagrant/airflow/dags"
DAG_TMPL = """
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 1, 1),
    "email": ["marimpis@brainvoyager.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("{{DAG_NAME}}", default_args=default_args, schedule_interval="@once")

t_sleep_dag = BashOperator(
    task_id="sleep",
    bash_command="sleep {{SLEEP_AMOUNT}}",
    dag=dag,
)

/*t_main_op = BashOperator(
    task_id="{{DAG_TASK_ID}}",
    bash_command="l",
    dag=dag,
)*/
"""


class ML_Train(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("sleep", type=str, required=True)
        parser.add_argument("dag_name", type=str, required=True)
        # parser.add_argument("task_id", type=str, required=True)
        args = parser.parse_args()

        dag = DAG_TMPL
        dag = dag.replace("{{DAG_NAME}}", args["dag_name"])
        dag = dag.replace("{{SLEEP_AMOUNT}}", args["sleep"])
        # dag = dag.replace("{{DAG_TASK_ID}}", args["task_id"])

        return json.dumps(dag)


api.add_resource(ML_Train, "/train/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
