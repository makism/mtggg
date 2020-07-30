import os

ROOT = "/mtgp/"  # os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLASK = os.path.abspath(os.path.join(ROOT, "web"))
DATASET = os.path.abspath(os.path.join(ROOT, "dataset"))
METAFLOW = os.path.abspath(os.path.join(ROOT, "metaflow"))
TEMP = "/tmp/"

ARTIFACTS = os.path.abspath(os.path.join(ROOT, "artifacts"))
OUTPUT_DATASET = os.path.abspath(os.path.join(ARTIFACTS, "dataset"))
SCRYFALL_IMAGES = os.path.abspath(os.path.join(ARTIFACTS, "scryfall_images"))
ML_MODELS = os.path.abspath(os.path.join(ARTIFACTS, "ml"))

DB_VERSIONING = os.path.abspath(os.path.join(ARTIFACTS, "versioning.db"))
SPARK_MODELS = os.path.abspath(os.path.join(ARTIFACTS, "spark_models"))

AIRFLOW_PROJECT_DIR = os.path.abspath(os.path.join(ROOT, "airflow"))
AIRFLOW_DAGS_DIR = "/home/vagrant/airflow/dags"
