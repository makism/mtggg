#!/usr/bin/env bash

# Source the proper Python environment
source ~/venv/bin/activate

export FLASK_APP=api.py
export FLASK_ENV="development"

# Start using Gunicorn
# gunicorn --bind 0.0.0.0:5500 wsgi:app

# Start using Flask's built-int server (for debugging)
# python api.py

# Start using directly Flask
flask run --host=0.0.0.0
