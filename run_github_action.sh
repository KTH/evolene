# Lägga dessa i en github actions.py enviro?
EVOLENE_DIRECTORY=/repo
WORKSPACE=/src
#echo "-- $GIT_COMMIT"

# REGISTRY_HOST=${{ secrets.EVOLENE_REGISTRY_HOST }}
# REGISTRY_USER=${{ secrets.EVOLENE_REGISTRY_USER }}
# REGISTRY_PASSWORD=${{ secrets.EVOLENE_REGISTRY_PASSWORD }}

# AZURE_REGISTRY_HOST=${{ secrets.EVOLENE_AZURE_REGISTRY_HOST }}
# AZURE_REGISTRY_USER=${{ secrets.EVOLENE_AZURE_REGISTRY_USER }}
# AZURE_REGISTRY_PASSWORD=${{ secrets.EVOLENE_AZURE_REGISTRY_PASSWORD }}

# NPM_USER=${{ secrets.NPM_USER }}
# NPM_PASSWORD=${{ secrets.NPM_PASSWORD }}
# NPM_EMAIL=${{ secrets.NPM_EMAIL }}

#!/bin/sh

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

# Run Evolene on the repository code.
#GIT_COMMIT=$GIT_COMMIT \
#GIT_BRANCH='master'\
#REGISTRY_HOST=$REGISTRY_HOST \
#REGISTRY_USER=$REGISTRY_USER \
#REGISTRY_PASSWORD=$REGISTRY_PASSWORD \
#AZURE_REGISTRY_HOST=$AZURE_REGISTRY_HOST \
#AZURE_REGISTRY_USER=$AZURE_REGISTRY_USER \
#AZURE_REGISTRY_PASSWORD=$AZURE_REGISTRY_PASSWORD \
#NPM_EMAIL=$NPM_EMAIL \
#NPM_USER=$NPM_USER \
#NPM_PASSWORD=$NPM_PASSWORD \
#BUILD_NUMBER=$(date +%s)  \
#WORKSPACE=$EVOLENE_DIRECTORY \
#EVOLENE_DIRECTORY=$EVOLENE_DIRECTORY \

# If its a npm pkg to build run npm login.
if [ -f "$WORKSPACE/npm.conf" ]; then
    $EVOLENE_DIRECTORY/npm_login.sh
    echo "Logged into NPM."
    cat $WORKSPACE/npm.conf
fi

npm whoami

if [ -f "~/.npmrc" ]; then
    echo "~/.npmrc exists."
fi

PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile pipenv run python $EVOLENE_DIRECTORY/run.py