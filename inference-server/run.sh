#!/bin/bash

# if ! [[ -d setup/venv ]]; then
#     cd setup && ./create_venv.sh && cd ..
# fi

# source setup/venv/bin/activate

gunicorn --reload --bind 0.0.0.0:7999 --config server/config/gunicorn.py "server.app:create_app()"