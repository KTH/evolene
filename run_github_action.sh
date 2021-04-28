# Lägga dessa i en github actions.py enviro?
EVOLENE_DIRECTORY=/repo
WORKSPACE=$EVOLENE_DIRECTORY
BUILD_NUMBER=$(date +%s) 

#!/bin/sh

# Print the version
echo "\n__________________________"
cat $EVOLENE_DIRECTORY/docker.conf
echo "\n__________________________\n"

# CD into the repository directory containing the source code to build (not Evolene).
cd /src

# Run Evolene on the repository code.
WORKSPACE=$EVOLENE_DIRECTORY EVOLENE_DIRECTORY=$EVOLENE_DIRECTORY PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile \
    pipenv run python $EVOLENE_DIRECTORY/run.py