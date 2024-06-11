#!/bin/bash

pip-compile setup.cfg

pip-sync requirements.txt

pip install pre-commit

pre-commit install
