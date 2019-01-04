#!/bin/bash

if [[ -d venv ]]; then
    rm -rf venv/
fi

virtualenv venv
source venv/bin/activate

pip3 install --upgrade pip
pip3 install -r ../requirements.txt