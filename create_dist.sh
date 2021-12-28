#!/bin/bash

set -e

pipenv install --dev
./run_tests.sh
pipenv run python setup.py sdist
