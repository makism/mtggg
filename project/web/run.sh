#!/usr/bin/env bash
source ~/venv/bin/activate

export FLASK_APP=web.py
export FLASK_ENV="development"

flask run --host=0.0.0.0 --port=5001
