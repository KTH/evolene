# Evolene :whale: ![alt text](https://api.travis-ci.org/KTH/evolene.svg?branch=master)

Automated builds of Docker images and npm packages

# What it is

Evolene runs a sequence of steps that build, test and in the end does a `docker push` on a SemVer tagged Docker image like `tamarack:2.3.40_f2486d7`. All steps including unit and integration
tests are run inside Docker containers, eliminating most Jenkins plugins.

It also supports npm package building and publishing.

Evolene uses Convention Over Configuration. That means that Evolene is configured by following standard naming convensions rather then per project configuration.

![Example of one-liner shell command in Jenkins](https://github.com/KTH/evolene/blob/master/images/jenkins.png)

# Requirements

For your app to be built using Evolene you need to have two files in your project root directory:

- `Dockerfile` - The build configuration file for the docker image

- `docker.conf` - A build metadata file used by evolene for versioning and naming. The example below will on the _40th_ build on Jenkins create `tamarack:2.3.40_f2486d7`. Where `f2486d7` is the git commit hash that triggered the build.

```bash
#
# Name to use when tagging the image
#
IMAGE_NAME=tamarack

#
# Evolene tags docker images using https://semver.org/ notation, major.minor.path.
#
# IMAGE_VERSION=major.minor
# The Patch is normally added by Evolene at build time using $BUILD_NUMBER
#

IMAGE_VERSION=2.3

#
# You can override using $BUILD_NUMBER as patch number for SemVer by
# explicitly adding it aswell.
# If this was set, the result whould be tamarack:2.3.0_f2486d7
#
# PATCH_VERSION=0

```

Now just add a "execute shell"-command to your jenkins job that looks like this:
`SLACK_CHANNELS=#my-channel $EVOLENE_DIRECTORY/run.sh`

or if you have no Slack

`$EVOLENE_DIRECTORY/run.sh`

_That is it!_ Evolene will tell you will all other things in your Slack channels or in the Jenkins console log, when you build your app.

:boom: :tada: Happy Coding!

# Features

- No configuration, unless you want it
- You need no Jenkins knowledge (almost), works on Jenkins, exactly as on your dev machine
- Supports unit and integration testing
- Semver for the win
- Handles all the Docker stuff
- Slack integrations of course
- Scan for passwords in your code
- ... and more

# Configuration

## Image name

Override the IMAGE_NAME in docker.conf for the image to build.

```bash
IMAGE_NAME='other-name'  $EVOLENE_DIRECTORY/run.sh
```

## Project Root

Build your project from an other directory.
If set the \$WORKSPACE set by Jenkins will be ignored.

```bash
PROJECT_ROOT='/other/jenkis/workspace/other-repo/'  $EVOLENE_DIRECTORY/run.sh
```

## Override Git Commit

Reuse a commit hash of the push that triggered the build.
If set the \$GIT_COMMIT set by Jenkins will be ignored.

```bash
GIT_COMMIT='abcdefhijkl1234456'  $EVOLENE_DIRECTORY/run.sh
```

## Specify Semver Patch Version

The patch version in the SemVer tag is the Jenkins $BUILD_NUMBER.
If set the $BUILD_NUMBER set by Jenkins will be ignored, and patch version
will always be tag tamarack:2.3.`40`.

Patch version can also be set in `docker.conf` with PATCH_VERSION=40

```bash
BUILD_NUMBER='40'  $EVOLENE_DIRECTORY/run.sh
```

## Build information to file

If you would like to get build information writen to a file. Set `BUILD_INFORMATION_OUTPUT_FILE` to a relative path
in your repo. Depending on the file extension a different file type will be created. (overwritten if it already exists).

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/version.js' $EVOLENE_DIRECTORY/run.sh
```

### Different file types

#### HTML

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/version.html' $EVOLENE_DIRECTORY/run.sh
```

```html
<!DOCTYPE html>
<html>
  <head>
    <title>About</title>
  </head>
  <body>
    <dl>
      <dt>gitBranch:</dt>
      <dd>origin/master</dd>
      <dt>gitCommit:</dt>
      <dd>f2486d79abf3af26225aa1dbde0fddfcd702c7e6</dd>
      <dt>gitUrl:</dt>
      <dd>git@gita.sys.kth.se:Infosys/tamarack.git</dd>
      <dt>jenkinsBuild:</dt>
      <dd>40</dd>
      <dt>jenkinsBuildDate:</dt>
      <dd>2018-10-31 12:49:14</dd>
      <dt>dockerName:</dt>
      <dd>tamarack</dd>
      <dt>dockerVersion:</dt>
      <dd>2.3.40_f2486d7</dd>
      <dt>dockerImage:</dt>
      <dd>kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7</dd>
    </dl>
  </body>
</html>
```

#### Javascript module

```bash
BUILD_INFORMATION_OUTPUT_FILE='/info.js'
```

```javascript
module.exports = {
  jenkinsBuildDate: "2018-10-31 12:49:14",
  dockerVersion: "2.3.40_f2486d7",
  jenkinsBuild: "40",
  dockerName: "tamarack",
  dockerImage: "kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7",
  gitCommit: "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  gitBranch: "origin/master",
  gitUrl: "git@github.com:KTH/tamarack.git",
};
```

#### Typescript

```bash
BUILD_INFORMATION_OUTPUT_FILE='/info.ts'
```

```javascript
exports const buildInfo {
  "jenkinsBuildDate": "2018-10-31 12:49:14",
  "dockerVersion": "2.3.40_f2486d7",
  "jenkinsBuild": "40",
  "dockerName": "tamarack",
  "dockerImage": "kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7",
  "gitCommit": "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  "gitBranch": "origin/master",
  "gitUrl": "git@github.com:KTH/tamarack.git"
}
```

#### JSON

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/info.json'
```

```json
{
  "jenkinsBuildDate": "2018-10-31 12:49:14",
  "dockerVersion": "2.3.40_f2486d7",
  "jenkinsBuild": "40",
  "dockerName": "tamarack",
  "dockerImage": "kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7",
  "gitCommit": "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  "gitBranch": "origin/master",
  "gitUrl": "git@github.com:KTH/tamarack.git"
}
```

#### Conf-file

```bash
BUILD_INFORMATION_OUTPUT_FILE='/info.conf'
```

```bash
jenkinsBuildDate=2018-10-31 12:49:14,
dockerVersion=2.3.40_f2486d7,
jenkinsBuild=40,
dockerName=tamarack,
dockerImage=kthregistryv2.sys.kth.se/tamarack:2.3.40_f2486d7,
gitCommit=f2486d79abf3af26225aa1dbde0fddfcd702c7e6,
gitBranch=origin/master
gitUrl=git@github.com:KTH/tamarack.git
```

# Testing

## Unit Testing

Add a file in the root of your project called `docker-compose-unit-tests.yml`.

Before unit tests are run, the image is built and its id is available to
the Docker Compose file via `$LOCAL_IMAGE_ID`.

One way is then to mount your tests directly into the docker images and run your tests on
that very image.

On your local machine you can run the same test using `ID=$(docker build -q .) && LOCAL_IMAGE_ID=$ID docker-compose -f docker-compose-unit-tests.yml up --build --abort-on-container-exit --always-recreate-deps --force-recreate`.

```yaml
version: "3"
services:
  web:
    build: .
    image: $LOCAL_IMAGE_ID
    # Mount and run tests.
    volumes:
      - ./tests:/tests
    command: ["sh", "-c", "npm install --development && npm test"]
```

## Integration Testing

Add a file in the root of your project called `docker-compose-integration-tests.yml`.
Before integration tests are run, the image is built and it´s id is availeble to
the Docker Compose file via `$LOCAL_IMAGE_ID`.

One way is then to start up your service and from other container run queries against
our server.

On your local machine you can run the same test using `ID=$(docker build -q .) && LOCAL_IMAGE_ID=$ID docker-compose -f docker-compose-integration-tests.yml up --build --abort-on-container-exit --always-recreate-deps --force-recreate`.

```yaml
version: "3"

services:
  web:
    build: .
    image: $LOCAL_IMAGE_ID
    environment:
      DB_URL: "mongodb://db:4444"
      DB_USER: "admin"
    ports:
      - 80
    depends_on:
      - db

  db:
    image: mongodb:latest
    ports:
      - 4444

  # Run curl commands from integration-tests against http://web:80
  integration-tests:
    build: ./tests/integration-tests
    depends_on:
      - web
```

# Publish NPM packages

Besides from working with docker images, Evolene also supports building and publishing npm packages.

## How to trigger

1. **Add a `/npm.conf` file** in the root of your repo. This file needs to contain the _node version_ to build the packet with.

```bash

# What version of node should be used?
# This is installed via nvm (https://github.com/creationix/nvm) on jenkins if missing
NODE_VERSION=10.14.2

# Do we allow npm audit to find criticals and let the build finish?
# Comment this out otherwise
# ALLOW_CRITICALS=0
```

2. Add a **script build** in your `package.json` that runs test (can be empty).

```json
"scripts": {
    "test": "./run_tests.sh",
    "build": "npm test"
  },
```

3. **Add a Jenkins job** that builds your package.

4. 🎉 Done!

Every time you push Evolene will run `npm run-script build`. After that Evolene will check ot see if the `version` in `package.json` have been updated. If it does not previously exists in the npm registry, a new version with this version number is published to [npm](https://registry.npmjs.org/).

Reminder: If you forget to update the version Evolene will run `npm run-script build`, but without publishing to the registy.

### Automaticly publish all builds

You can configure your npm packages to publish to npm registy on every commit. This is done by adding a `"automaticPublish": "true"` in the root of the **package.json**. This will make Evolene look in the npm registry for the latest published version that matches "major.minor" and incrementing the patch version by one.

```json
{
  "version": "1.0.2",
  "automaticPublish": "true",
}

```

Example: If you have version: 1.0.2, Evolene will look for the latest version 1.0, in this example 1.0.9. Increment patch version to 10, and push 1.0.10.

![Published package are shown in Slack](https://github.com/KTH/evolene/blob/master/images/npm.png)

### Build information added to NPM packages automatically

Inside every npm-package there is a js-module file `/build-information.js` that contains:

```javascript
module.exports = {
  "jenkinsBuildDate": "2018-10-31 12:49:14",
  "jenkinsBuild": "40",
  "gitCommit": "f2486d79abf3af26225aa1dbde0fddfcd702c7e6",
  "gitBranch": "origin/master"
  "gitUrl": "git@github.com:KTH/my-npm-package.git"
}
```

## Environment variables for setting up NPM publish on Jenkins

- NPM_USER - The user to use for npm publish
- NPM_PASSWORD - The password to use for npm publish
- NPM_EMAIL - The email to use for npm publish

# Slack Integration

## Slack web hook

The Slack webhook endpoint where the `SLACK_CHANNELS` can be found.

```bash
SLACK_WEB_HOOK='https://hooks.slack.com/services/1234asdfasd/' $EVOLENE_DIRECTORY/run.sh
```

## Slack channels to post build information to

Comma separated list of channels to post messages to. Messages are build inforation,
failures an push information.

```bash
SLACK_CHANNELS='#pipeline-logs,#devops' $EVOLENE_DIRECTORY/run.sh
```

# Security scaning

By default files in your repo will be scanned for strings that looks like passwords or tokens. We use [RepoSupervisor](https://github.com/auth0/repo-supervisor/) for this.

When your project is built a warning will be sent to SLACK_CHANNELS with the files that contain suspisious files. If a file gives you a false possitive, you can create a file in the root of your repository and name it `.scanignore`. In the .scanignore file you can add catalogs or files that the security scan should ignore.

## .scanignore formatting

```bash
# Catalogs starting with, or specific files.
/node_modules/
/imported-data/personnumer.txt
```

# Docker Registries

## Private Docker Registry

Unless `PUSH_PUBLIC` is set to `true`, this registry will be used.
The host without protocol.

```bash
REGISTRY_HOST='private-docker-registry.mycompany.com' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registry User

The private `REGISTRY_HOST`:s BASIC_AUTH user who has the rights to read and push to the private registry.

```bash
REGISTRY_USER='myuser' $EVOLENE_DIRECTORY/run.sh
```

### Private Docker Registry Password

The private `REGISTRY_HOST`:s BASIC_AUTH users password.

```bash
REGISTRY_PASSWORD='qwerty123' $EVOLENE_DIRECTORY/run.sh
```

## Public repository

Set to `true` When you whant to push your image to `hub.docker.com/r/kthse`. This will push two tags,
the ususual SemVer with commit `tamarack:2.3.40_f2486d7`, but also and also a short tag with only SemVer `tamarack:2.3.40`. This is done to enable reuse of tags.

```bash
PUSH_PUBLIC='True' # Set or unset
```

## Other envs

### Skip dry run step

Normally Evolene does a `docker run IMAGE_ID` to see that the image is build correctly and can start.
Some images does not support this (os-images) and therefor exits causing the pipeline to exit.

```bash
SKIP_DRY_RUN='True' # Set or unset
```

### Feature flag for building

Sometimes we add new features that are sort of in beta. If you would like to try these out allow
exprimental.

```bash
EXPERIMENTAL='True' # Set or unset
```

### Current Evolene running

Path to the directory of a Evolene dist version.
Used in Jenkin builds for shorter path when envoking the Evolene itself `$EVOLENE_DIRECTORY/run.sh`.
Also gives you a way of specifing what version of Evolene that is used.

```bash
EVOLENE_DIRECTORY='/var/lib/jenkins/workspace/evolene/dist/evolene-1.6'
```

### Send build arguments to the docker build

Sometimes you need to send information to the docker build stage, for example to set a specific maven settings.xml
file. You can do this by setting the environment variable `DOCKER_BUILD_ARGS`
to a comma separated string of arguments on the format `ARG=VALUE` and configuring your Dockerfile with `ARG DOCKER_BUILD_ARG`. See example below.

```bash
DOCKER_BUILD_ARGS='MAVEN_SETTINGS=<?xml version="1.0" encoding="UTF-8"?> <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd"> <servers> <server> <id>dev-azure-com-kth-integration-integration</id> <configuration><httpHeaders> <property> <name>Authorization</name> <value>Basic password=</value> </property> </httpHeaders> </configuration> </server></servers></settings>,ANOTHER_SETTING=blabla'
```

```dockerfile
ARG MAVEN_SETTINGS
ARG ANOTHER_SETTING
RUN echo MAVEN_SETTINGS >/usr/share/maven/conf/settings.xml
```

# Handling of none master/main branches
Only main branch (master) will be pushed to NPM or Docker registries. Other branches will build and tested. Just not the last step, published.

# Setup Evolene on Jenkins

## 1. Add default envs for builds on the Jenkins server

We recommend that the following envs are available to each Jenkins job. The can be overridden by
env arguments per build as shown above.

```bash
EVOLENE_DIRECTORY='/var/lib/jenkins/workspace/evolene/dist/evolene-1.6'
SLACK_WEB_HOOK='https://hooks.slack.com/services/1234asdfasd/'
REGISTRY_HOST='private-docker-registry.mycompany.com'
REGISTRY_PASSWORD='very-secret-pwd'
REGISTRY_USER='jenkins-ci'
```

## 2. Set up a build task that builds Evolene

1. Add a new job that pulls the Evolene source

2. Add a _Execute shell_ step

```bash
/create_dist.sh
LATEST_DIST=$(ls -tp dist | grep -v / | head -1)
tar xvf dist/$LATEST_DIST -C dist
rm -rf dist/latest
mkdir dist/latest
tar xvf dist/$LATEST_DIST -C dist/latest --strip 1
chmod -R 700 dist/latest
```

3. Run the Jenkins job. This will create a executable Evolene dist in `/var/lib/jenkins/workspace/evolene/dist/evolene-1.6`.

## 3. Test your setup

Test your setup by adding a Docker application that follows Evolene [Usage Requirements](https://gita.sys.kth.se/Infosys/evolene/blob/master/README.md#exclamation-user-requirements) and run a _Execute shell_.
`$EVOLENE_DIRECTORY/run.sh`

# Setup Evolene for development

## Run locally

```bash
python run.py docker run-pipeline
```

## Create a distribution

Note! The version of the dist is defined in `setup.py`

```bash
./create_dist.sh`
```

## Run unit tests

```bash
./run_tests.sh
```
