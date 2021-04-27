FROM kthse/kth-python:3.8.0

RUN mkdir /repo

WORKDIR /repo

RUN apk update && \
    apk upgrade && \
    apk add --no-cache bash gcc libc-dev libxslt-dev libxslt py-pip docker && \
    rm -rf /var/cache/apk/*
        
COPY Pipfile Pipfile

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN pipenv install pip

RUN pipenv install

COPY ["modules",  "modules"]
COPY ["run.py", "run.py"]
COPY ["run_github_action.sh", "run_github_action.sh"]
COPY ["docker.conf",  "docker.conf"]

ENV EVOLENE_DIRECTORY /repo

RUN mkdir src

CMD ["/bin/sh", "-c", "/repo/run_github_action.sh"]
