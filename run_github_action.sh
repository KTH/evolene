#!/bin/sh

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

# If its a npm pkg to build run npm login.
if [ -f "npm.conf" ]; then
    $EVOLENE_DIRECTORY/npm_login.sh > /dev/null 2>&1
    echo "Logged into NPM."
fi

echo ""
echo "*****************************************************************"
echo ""
npm whoami
echo ""
echo "*****************************************************************"

PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile pipenv run python $EVOLENE_DIRECTORY/run.py