# Lägga dessa i en github actions.py enviro?
EVOLENE_DIRECTORY=/repo
WORKSPACE=$EVOLENE_DIRECTORY
BUILD_NUMBER=$(date +%s) 
GIT_COMMIT=$GITHUB_SHA
GIT_BRANCH='master'

echo ${{secrets.EVOLENE_AZURE_REGISTRY_USER}}

REGISTRY_HOST: ${{secrets.EVOLENE_REGISTRY_HOST}}
REGISTRY_USER: ${{secrets.EVOLENE_REGISTRY_USER}}
REGISTRY_PASSWORD: ${{secrets.EVOLENE_REGISTRY_PASSWORD}}

AZURE_REGISTRY_HOST: ${{secrets.EVOLENE_AZURE_REGISTRY_HOST}}
AZURE_REGISTRY_USER: ${{secrets.EVOLENE_AZURE_REGISTRY_USER}}
AZURE_REGISTRY_PASSWORD: ${{secrets.EVOLENE_AZURE_REGISTRY_PASSWORD}}

NPM_USER: ${{secrets.NPM_USER}}
NPM_PASSWORD: ${{secrets.NPM_PASSWORD}}
NPM_EMAIL: ${{secrets.NPM_EMAIL}}

#!/bin/sh

# Print the version
echo "__________________________"
cat $EVOLENE_DIRECTORY/docker.conf
echo "__________________________"

# CD into the repository directory containing the source code to build (not Evolene).
cd /src

# Run Evolene on the repository code.
GIT_BRANCH=$GIT_BRANCH BUILD_NUMBER=$BUILD_NUMBER WORKSPACE=$EVOLENE_DIRECTORY EVOLENE_DIRECTORY=$EVOLENE_DIRECTORY PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile \
    pipenv run python $EVOLENE_DIRECTORY/run.py