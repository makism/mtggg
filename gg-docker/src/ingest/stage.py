import glob
import json
import pathlib
import tqdm

from mtggg.config import RAW_DATA, STAGE_DATA

if __name__ == "__main__":
    for f in tqdm.tqdm(glob.glob(f"{RAW_DATA}/*.json")):
        p = pathlib.Path(f)

        cards = None
        with open(p, "r") as fp:
            raw_data = json.load(fp)
            cards = raw_data["data"]["cards"]

            fname = f"{STAGE_DATA}/{p.name}"
            with open(fname, "w") as fp:
                json.dump(cards, fp)
