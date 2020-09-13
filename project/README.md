# Project organization

> Main Application

| Namespace          | Description                   |   |
|--------------------|-------------------------------|---|
| `airflow/`         | Airflow DAG templates         |   |
| `api/`             | REST-API application          | 🌟|
| `config/`          | Configuration & settings      |   |
| `metaflow/`        | All the pipelines in MetaFlow | 🌟|
| `ml/`              | Machine Learning models       | 🌟|
| `web/`             | A *WIP* Flask application | |

> Runtime-specific Resources

| Namespace          | Description                                   |
|--------------------|-----------------------------------------------|
| `artifacts/`       | Generated models and intermmediate results    |
| `assets/`          | Assets and images used                        |
| `dataset/`         | Dataset files; fetch from an external sosurce |
| `logs/ `           | Well... logs...                               |

> Development and Research Applications

| Namespace          | Description           | |
|--------------------|-----------------------|--------|
| `cli/`             | ES example queries    | |
| `data_prep_eda/`   | | |
| `dev/`             | Development Jupyter Notebooks| 🌟 |
| `docs/`            | |
| `NLP experiments/` | NLP experiments       | |
| `kafka_stream/`    | Kafka experiments     | |


> Legend

| Marker |   |
|--------|---|
| 🌟     | Check it out! |


# Requirements

If needed, you may install all the required packages with `pip3`as follows:

```bash
pip3 install -r requirements.txt
```

# Dataset

Fetch the JSON files with:

```bash
cd dataset
./fetch.sh
```

It will download a few JSON files in the `dataset/` directory.

# Configuration

If you are planning to use the project outside the Vagrant box, you will have to modify the file `config/config.py` and set the variable `ROOT` accordingly.

# Dateset preparation

Now, we'll fetch the cards and drop some metadata from the JSON files.

```bash
cd metaflow
python prepare_cards.py run --keyruneCodes 'THB,ELD'
```

# Preprocessing

The next step is to perform an initial preprocessing and extract only the cards from the JSON files.

```bash
python preprocess_cards.py run --keyruneCodes 'THB,ELD' --cleanUp 'all'
```

# Export

As soon as we have preprocessed our dataset sucessfuly, we can export it to MongoDB and ElasticSearch to support the REST-API backend of our project.

```bash
python export_cards.py run --keyruneCodes 'THB,ELD' --cleanUp 'all'
```

# Images
We can also generate DAGs for each dataset to fetch their images. Each DAG will be submitted to Apache Airflow paused.

The downloaded images will be stored in `artifacts/scryfall_images/`.

```bash
python prepare_dags.py run --keyruneCodes 'THB,ELD'
```

Each DAG will keep track of its status in a collection in MongoDB.

# REST-API

We use Gunicorn as a WSGI server, however for development purposes we optionaly use the default Flask server.

Explore the configuration in `api/run.sh` for your options, and run the application with:

```bash
cd api/
source run.sh
```

# EDA

During the development and analysis numerous Jupyter Notebooks were developed,
which are available at `dev/`, `data_prep_eda/` and `NLP/`. The resulting code is
mainstreamed and backported into the main application.

# Web interface

You may start the web application using Flask's built-in web server with:

```bash
cd web/
source run.sh
```
