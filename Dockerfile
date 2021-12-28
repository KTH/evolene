FROM ubuntu:20.04

RUN mkdir /repo

WORKDIR /repo

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq python3 curl docker.io gcc git zip pipenv && \
    apt-get clean
        
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN pipenv install

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

COPY ["modules",  "modules"]
COPY ["run.py", "run.py"]
COPY ["run_github_action.sh", "run_github_action.sh"]
COPY ["docker.conf",  "docker.conf"]
COPY ["version.conf",  "version.conf"]

ENV EVOLENE_DIRECTORY /repo

RUN mkdir src
WORKDIR /src

CMD ["/bin/bash", "-c", "/repo/run_github_action.sh"]
