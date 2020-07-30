# pylint: disable-all
import json
import os.path
from metaflow import FlowSpec, Parameter, step
from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime as dt
import shutil

import config
import preprocess_fn
from mf_common_base import MF_Common_Base


class PrepareDags(FlowSpec, MF_Common_Base):
    @step
    def start(self):
        """ Begin here. """

        self.parse_keyruneCodes(ftype="parquet")

        self.next(self.create_dag, foreach="list_keyruneCodes")

    @step
    def create_dag(self):
        """ Read data. """

        self.code = self.input
        parquet_file = f"{config.OUTPUT_DATASET}/{self.input}_cards.parquet"

        output_dir = f"{config.SCRYFALL_IMAGES}/{self.code}/"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        tpl_file = "fetch_images.py.tpl"

        env = Environment(loader=FileSystemLoader(f"{config.AIRFLOW_PROJECT_DIR}"))
        tpl = env.get_template(tpl_file)

        spark = preprocess_fn.spark_session()
        df = spark.read.parquet(parquet_file)
        l = df.select("scryfallId").collect()

        dt_now = dt.now()

        dag = tpl.render(
            dag_name=f"dag_{self.code}",
            parse_datetime=dt_now,
            conf_dt_Y=dt_now.year,
            conf_dt_m=dt_now.month,
            conf_dt_d=dt_now.day,
            conf_user_name=f"mtggg_{self.code}",
            all_scryids=l,
            keyruneCode=self.code,
        )

        with open(f"/tmp/dag_{self.code}.py", "w") as fp:
            fp.write(dag)

        src_dag = f"/tmp/dag_{self.code}.py"
        # dst_dag = f"{config.AIRFLOW_DAGS_DIR}/M20_dag.py"
        dst_dag = f"/home/vagrant/airflow/dags/{self.code}_fetch_images.py"
        shutil.copy(src=src_dag, dst=dst_dag)

        self.next(self.join)

    @step
    def join(self, inputs):
        """Join our parallel branches."""

        self.next(self.end)

    @step
    def end(self):
        """ Finalize and clean up. """

        print("All done.")


if __name__ == "__main__":
    PrepareDags()
