#!/bin/sh

cd /src
EVOLENE_DIRECTORY=$EVOLENE_DIRECTORY PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile \
    pipenv run python $EVOLENE_DIRECTORY/run.py