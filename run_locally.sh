#!/bin/bash

DEBUG=True \
GIT_COMMIT=abc1237XXXXX \
BUILD_NUMBER=123 \
WORKSPACE=/Users/tinglev/Repos/evolene/test/data \
IMAGE_NAME=evolene \
REGISTRY_HOST=kthregistryv2.sys.kth.se \
REGISTRY_USER=jenkins \
SLACK_CHANNELS=#pipeline-logs \
EVOLENE_SLACK_WEB_HOOK=https://not_at_this_time \
EVOLENE_DIRECTORY=$(pwd) \
pipenv run python run.py docker run-pipeline
