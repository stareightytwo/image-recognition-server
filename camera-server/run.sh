#!/bin/bash

if ! [[ -d venv ]]; then
    cd setup && ./create_venv.sh && cd ..
fi

source setup/venv/bin/activate

gunicorn --reload --config server/configs/gunicorn_config.py "server.app:create_app()"
