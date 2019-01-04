SHELL := /bin/bash

.PHONY: help
help:
	@echo "    init-venv"
	@echo "         Initializes the python virtual environment. Requires virtualenv."


.PHONY: init-venv
init-venv:
	virtualenv venv;\
	source venv/bin/activate;\
	pip install -r requirements.txt

