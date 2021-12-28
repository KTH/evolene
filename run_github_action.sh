#!/bin/bash

EVOLENE_DIRECTORY=/repo
WORKSPACE=/src

# Print the version
echo ""

echo "*****************************************************************"
echo "*   Evolene Ci/CD environment https://github.com/kth/evolene    *"
echo "*****************************************************************"
cat $EVOLENE_DIRECTORY/version.conf
echo ""
echo "*****************************************************************"
echo ""
# CD into the repository directory containing the source code to build (not Evolenes).
cd $WORKSPACE

PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile pipenv run python $EVOLENE_DIRECTORY/run.py
