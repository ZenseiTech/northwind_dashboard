#!/bin/bash

export FLASK_APP=northwind.py

export FLASK_DEBUG=1

flask shell

# Commands:
#     run     Runs as development server.
#     shell   Runs a shell in the app context.

# flask db migrate -m 'Some comment'

# flask db upgrade

# or

# flask db downgrade
