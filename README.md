```
███╗   ███╗████████╗ ██████╗      ██████╗  ██████╗ 
████╗ ████║╚══██╔══╝██╔════╝     ██╔════╝ ██╔════╝ 
██╔████╔██║   ██║   ██║  ███╗    ██║  ███╗██║  ███╗
██║╚██╔╝██║   ██║   ██║   ██║    ██║   ██║██║   ██║
██║ ╚═╝ ██║   ██║   ╚██████╔╝    ╚██████╔╝╚██████╔╝
╚═╝     ╚═╝   ╚═╝    ╚═════╝      ╚═════╝  ╚═════╝ 
```
## Getting started

First build the images,
```bash
./build.sh
```

then, spin the Apache Spark cluster (127.0.0.1:4040) and the Jupyter notebook server (127.0.0.1:8888),
```bash
docker-compose up -d
```

## Fetch data

You may fetch the raw data with:

```bash
docker exec -it jupyterlab scripts/fetch_data.sh
```

Then, apply a very basic preprocessing with

```bash
docker exec -it jupyterlab python src/ingests/stage.py
```
