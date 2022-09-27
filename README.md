```

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▀▄░█▄░▄█░▄▄▄██░▄▄░██░▄▄░██
█░█▄█░██░██░█▄▀██░█▀▀██░█▀▀██
█▄███▄██▄██▄▄▄▄██░▀▀▄██░▀▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

```

First fetch the data from the API:

```bash
scripts/fetch_data.sh
```

Then, apply a very basic preprocessing with

```bash
python src/ingests/stage.py
```