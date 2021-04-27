EVOLENE_DIRECTORY=/repo
#!/bin/sh

# Print the version
cat $EVOLENE_DIRECTORY/docker.conf

# CD into the repository directory containing the source code to build (not Evolene).
cd /src

# Run Evolene on the repository code.
EVOLENE_DIRECTORY=$EVOLENE_DIRECTORY PIPENV_PIPFILE=$EVOLENE_DIRECTORY/Pipfile \
    pipenv run python $EVOLENE_DIRECTORY/run.py