# Setup

- - -


## Dataset

Fetch the JSON files with:

```
cd dataset
./fetch.sh
```

It will download a few JSON files in the `dataset` directory.

## Preprocess

The next step is to perform an initial preprocessing and extract only the cards from the JSON files.

```
cd metaflow
python preprocess_cards.py run --keyruneCodes 'THB,ELD'
```

## EDA

## Spark
```
