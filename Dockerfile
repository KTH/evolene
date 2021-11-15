FROM kthse/kth-python:3.10.0

RUN mkdir /repo

WORKDIR /repo

RUN apk update && \
    apk upgrade && \
    apk add --no-cache  \
        bash  \
        gcc  \
        libc-dev  \
        libxslt-dev  \
        libxslt  \
        py-pip  \
        docker  \
        make  \
        libffi-dev  \
        linux-headers  \
        llvm10  \
        cargo  \
        openssl-dev  \
        build-base  \
        openssh  \
        git  \
        curl  \
        nodejs  \
        npm  \
        zip && \
    rm -rf /var/cache/apk/*
        
COPY Pipfile Pipfile

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN pipenv install

RUN pipenv install pip
RUN pip install docker-compose

RUN touch /root/.bash_profile
RUN touch /root/.bashrc
RUN touch /root/.profile

RUN mkdir /root/.nvm

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

RUN cat /root/.bashrc > /root/.bash_profile > /root/.profile

COPY ["modules",  "modules"]
COPY ["run.py", "run.py"]
COPY ["run_github_action.sh", "run_github_action.sh"]
COPY ["docker.conf",  "docker.conf"]
COPY ["version.conf",  "version.conf"]


ENV EVOLENE_DIRECTORY /repo

RUN mkdir src
WORKDIR /src

CMD ["/bin/bash", "-c", "/repo/run_github_action.sh"]
