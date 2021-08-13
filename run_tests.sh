#!/bin/sh

if [[ -n "${UNIT_TESTS_IN_DOCKER}" ]]; then
  echo "Running unit tests from docker-compose-unit-tests.yml"
  # Inside the Evolene Dockerfile source files are in /repo.
  # But the WORKDIR is in /src where we mount the repositories to build with Evolene.
  cd /repo
  pipenv install --dev
  PIPENV_VERBOSITY=-1 WORKSPACE=./test/data pipenv run green -vv --run-coverage --failfast "test"
  exit 0
fi

if [[ -n "${INSTALL}" ]]; then
  echo "Installing ... ${INSTALL}"
  pipenv install --dev 
fi

echo "To install deps, run: INSTALL=True ./run_tests.sh"
PIPENV_VERBOSITY=0 WORKSPACE=./test/data pipenv run green --failfast "test"


