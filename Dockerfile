FROM kthse/kth-python:3.8.0

RUN mkdir /repo && \
    mkdir /repo/secrets && \
    mkdir /repo/certs && \
    mkdir -p /root/.ssh

WORKDIR /repo

RUN apk update && \
    apk upgrade && \
    apk add --no-cache bash \
    docker musl-dev libffi-dev libressl-dev libxml2 libxslt libxslt-dev && \
    apk add py-pip && \
    rm -rf /var/cache/apk/*
        
COPY Pipfile Pipfile

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN pipenv install pip

RUN pipenv install

COPY ["modules",  "modules"]
COPY ["run.py", "run.py"]

CMD ["pipenv", "run", "python", "-u", "run.py"]