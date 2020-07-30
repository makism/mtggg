# Setup

- - -

### Dataset

Fetch the JSON files with:

```
cd dataset
./fetch.sh
```

It will download a few JSON files in the `dataset` directory.

### Configuration

If you are planning to use the project outside the Vagrant box, you will have to modify the file `config/config.py` and set the variable `ROOT` accordingly.

## Dateset preparation

Now, we'll fetch the cards and drop some metadata from the JSON files.

```
cd metaflow
python prepare_cards.py run --keyruneCodes 'THB,ELD'
```

### Preprocessing

The next step is to perform an initial preprocessing and extract only the cards from the JSON files.

```
python preprocess_cards.py run --keyruneCodes 'THB,ELD' --cleanUp 'all'
```

### Export

As soon as we have preprocessed our dataset sucessfuly, we can export it to MongoDB and ElasticSearch to support the REST-API backend of our project.

```
python export_cards.py run --keyruneCodes 'THB,ELD' --cleanUp 'all'
```

### Images
We can also generate DAGs for each dataset to fetch their images. Each DAG will be submitted to Apache Airflow paused.

```
python prepare_dags.py run --keyruneCodes 'THB,ELD'
```

Each DAG will keep track of its status in a collection in MongoDB.

- - -

# Web interface

- - -

# REST-API

- - -

# EDA
