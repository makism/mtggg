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
import config
import logger

log_handler = logger.get_logger(logger_name="metaflow_prepare_dags")

API_ENDPOINT = "https://api.scryfall.com/cards/"

default_args = {
    "owner": "mtggg",
    "start_date": datetime({{ conf_dt_Y }}, {{ conf_dt_m }}, {{ conf_dt_d }}),
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("{{ dag_name }}", default_args=default_args, schedule_interval="@once")

def fetch_image(scryid):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mtggg"]
    col = db["dags"]
    col2 = db['images']

    new_dag = col.insert_one({"scryid": scryid, "set": "{{ keyruneCode }}", "when": datetime.now(), "status": "queued"})

    log_handler.info(f"call fetch_image: {scryid} ({{ keyruneCode }})")

    query_url = API_ENDPOINT + scryid
    r = requests.get(query_url)
    json = r.json()

    images_uri = json['image_uris']
    image_png = images_uri['png']
    image_crop = images_uri['art_crop']

    output_dir = f"{config.SCRYFALL_IMAGES}/{{ keyruneCode }}/"
    output_png = f"{output_dir}/{scryid}.png"
    output_crop = f"{output_dir}/{scryid}_crop.png"

    if not os.path.exists(output_png):
        r = requests.get(image_png, stream=True)
        if r.status_code == 200:
            log_handler.info(f"fetch_image - fetched png image for {scryid}")
            with open(output_png, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            new_png = col2.insert_one({"scryid": scryid, "set": "{{ keyruneCode }}", "when": datetime.now(), "artifact": "png"})

    if not os.path.exists(output_crop):
        r = requests.get(image_crop, stream=True)
        if r.status_code == 200:
            log_handler.info(f"fetch_image - fetched cropped image for {scryid}")
            with open(output_crop, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            new_crop = col2.insert_one({"scryid": scryid, "set": "{{ keyruneCode }}", "when": datetime.now(), "artifact": "crop"})

    update_dag = col.update({"scryid": scryid}, {"scryid": scryid, "when": datetime.now(), "status": "completed"})
    #update_dag = col.insert_one({"scryid": scryid, "set": "{{ keyruneCode }}", "when": datetime.now(), "status": "completed"})

    return True

{% for scryid in all_scryids %}
t_{{ loop.index }} = PythonOperator(task_id="{{ loop.index }}",
    python_callable=fetch_image,
    op_kwargs={"scryid": "{{ scryid[0] }}" },
    dag=dag,
    )
{% endfor %}
