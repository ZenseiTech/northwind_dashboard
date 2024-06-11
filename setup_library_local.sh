#!/bin/bash

pip-compile requirements_local.in

pip-sync requirements_local.txt

pip-compile setup.cfg

pip-sync requirements.txt

pip install pre-commit

pre-commit install
