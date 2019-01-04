#!/bin/bash

if [[ -d venv ]]; then
    rm -rf venv/
fi

virtualenv venv
source venv/bin/activate

pip3 install --upgrade pip
pip3 install -r ../requirements.txt

if ! [[ -d darkflow ]]; then
	git clone https://github.com/thtrieu/darkflow.git
	cd darkflow

	pip3 install .
fi

# TODO: install tensorflow