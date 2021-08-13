#!/bin/sh

if [[ -z "${SKIP_INSTALL}" ]]; then
  echo "To skip install run: SKIP_INSTALL=True ./run_tests.sh"
  pipenv install --dev 
fi

if [[ -z "${SHORT}" ]]; then
  echo "To get minimal ouput run: SHORT=True SKIP_INSTALL=True ./run_tests.sh"
  #PIPENV_VERBOSITY=-1 WORKSPACE=./test/data pipenv run green -vv --run-coverage --failfast "test"
  PIPENV_VERBOSITY=0 WORKSPACE=./test/data pipenv run green --failfast "test"
else
  PIPENV_VERBOSITY=-1 WORKSPACE=./test/data pipenv run green --failfast "test"
fi
