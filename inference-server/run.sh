#!/bin/bash

if ! [[ -d setup/venv ]]; then
    cd setup && ./create_venv.sh && cd ..
fi

source setup/venv/bin/activate

gunicorn --reload --config server/configs/gunicorn_config.py "app"