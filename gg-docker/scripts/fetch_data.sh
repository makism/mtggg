#!/bin/bash

BASE_URL="https://mtgjson.com/api/v5"
DEST_DIR=$PWD/data/raw

wget "https://mtgjson.com/api/v5/DMU.json" -O /data/raw/DMU.json

wget "https://mtgjson.com/api/v5/M22.json" -O /data/raw/M22.json

wget "https://mtgjson.com/api/v5/M21.json" -O /data/raw/M21.json

wget "https://mtgjson.com/api/v5/IKO.json" -O /data/raw/IKO.json

wget "https://mtgjson.com/api/v5/THB.json" -O /data/raw/THB.json

wget "https://mtgjson.com/api/v5/ELD.json" -O /data/raw/ELD.json

wget "https://mtgjson.com/api/v5/M20.json" -O /data/raw/M20.json

wget "https://mtgjson.com/api/v5/WAR.json" -O /data/raw/WAR.json
