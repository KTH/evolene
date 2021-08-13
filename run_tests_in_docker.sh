#!/bin/bash

echo "Running unit tests inside 🐳 Docker Compose"

ID=$(docker build -q .) && \
    WORKSPACE=$(pwd) LOCAL_IMAGE_ID=$ID \
    docker-compose \
        --file docker-compose-unit-tests.yml up \
        --force-recreate \
        --abort-on-container-exit \
        --always-recreate-deps \
        --no-log-prefix \
        --quiet-pull \
        --build
    