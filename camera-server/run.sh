#!/bin/bash

source setup/venv/bin/activate

gunicorn --reload --config server/configs/gunicorn_config.py "server.app:create_app()"