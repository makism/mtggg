from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    create_engine,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy
import numpy as np
import os
from datetime import datetime

import config
import logger


Base = declarative_base()


log_handler = logger.get_logger(logger_name="versioning")


class SparkModelsVersions(Base):
    __tablename__ = "spark_models_versions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    model = Column(String(255))
    version = Column(Integer)
    filename = Column(String(255))
    hash = Column(String(255))


def versioning_db_init():
    if not os.path.exists(config.DB_VERSIONING):
        engine = create_engine(f"sqlite:///{config.DB_VERSIONING}")
        Base.metadata.create_all(engine)

        log_handler.info(f"Created db {config.DB_VERSIONING}.")
    else:
        log_handler.info(f"DB {config.DB_VERSIONING} exists.")


def versioning_register(mdl):
    engine = create_engine(f"sqlite:///{config.DB_VERSIONING}")
    metadata = sqlalchemy.MetaData()
    connection = engine.connect()
    tbl = sqlalchemy.Table(
        "spark_models_versions", metadata, autoload=True, autoload_with=engine
    )

    q = (
        tbl.select()
        .where(tbl.columns.model == "mdl")
        .order_by(text("date desc"))
        .limit(1)
    )
    r = connection.execute(q)
    rows = r.fetchall()

    dt = datetime.now()
    if len(rows) == 0:
        q = tbl.insert().values(
            date=dt,
            model=mdl["name"],
            version="1",
            filename=mdl["fname"],
            hash=mdl["hash"],
        )
        r = connection.execute(q)
    else:
        previous_version = np.int32(rows[0][3])
        new_version = previous_version + 1

        q = tbl.insert().values(
            date=dt,
            model="mdl",
            version=str(new_version),
            filename="",
            hash="0123456789ABBCF",
        )
        r = connection.execute(q)


if __name__ == "__main__":
    mdl = {"name": "some name", "fname": "spark_encoder.pkl", "hash": "0123456789ABBCF"}

    versioning_db_init()
    versioning_register(mdl)
