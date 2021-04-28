# Lägga dessa i en github actions.py enviro?
EVOLENE_DIRECTORY=/repo
WORKSPACE=$EVOLENE_DIRECTORY
BUILD_NUMBER=$(date +%s) 

#!/bin/sh

# Print the version
echo "__________________________"
cat $EVOLENE_DIRECTORY/docker.conf
echo "__________________________"

# CD into the repository directory containing the source code to build (not Evolene).
cd /src

# Run Evolene on the repository code.
BUILD_NUMBER=$BUILD_NUMBER WORKSPACE=$EVOLENE_DIRECTORY EVOLENE_DIRECTORY=$EVOLENE_DIRECTORY PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile \
    pipenv run python $EVOLENE_DIRECTORY/run.py