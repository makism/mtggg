# created on: {{ parse_datetime }}

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os.path
import time
import requests
from pymongo import MongoClient

import sys
sys.path.append("/mtgp/config/")
sys.path.append("/mtgp/ml/")
import config
import logger

from tf_rnn import tf_rnn_predict

log_handler = logger.get_logger(logger_name="rest_api_generate")

default_args = {
    "owner": "{{ conf_user_name }}",
    "start_date": datetime({{ conf_dt_Y }}, {{ conf_dt_m }}, {{ conf_dt_d }}),
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("{{ dag_name }}", default_args=default_args, schedule_interval="@once")

def generate_name(uuid):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mtggg"]
    col = db["api_jobs"]
    col2 = db["api_results"]

    new_job = col.insert_one({
        "uuid": uuid,
        "when": datetime.now(),
        "status": "queued"
    })

    log_handler.info(f"ml generate random for uuid: {uuid}")

    model_weights = f"{config.ML_MODELS}/rnn_all_sets.h5"
    corpus_file = f"{config.ML_MODELS}/card_names.txt"

    result = tf_rnn_predict(model_weights, corpus_file)

    update_dag = col.update({"uuid": uuid}, {
        "uuid": uuid,
        "when": datetime.now(),
        "status": "completed"
    })

    result_dag = col2.insert_one({
        "uuid": uuid,
        "when": datetime.now(),
        "response": result
    })

    return True

task = PythonOperator(task_id="1",
    python_callable=generate_name,
    op_kwargs={"uuid": "{{ uuid }}" },
    dag=dag,
    )
