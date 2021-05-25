# Docker Pipeline Specific Configurations

The Docker pipeline will start running if you add add a `/Dockerfile` in the root of your code repository.

This will invoke the common steps we run on all source code, and then check, build and test you Docker project. As always there is no need to check the CI logs, anything Evolene dont like will be sent to your Slack channels with information about how to fix it :).

# Docker pipeline requirements

For your app to be built using Evolene you need to have two files in your project root directory:

- `Dockerfile` - The build configuration file for the docker image.
- `docker.conf` - A build metadata file used by evolene for versioning and naming.

The example below will on the build on Jenkins create `tamarack:2.3.1621960803_f2486d7`. Where `f2486d7` is the git commit hash that triggered the build, and the patch-versoin `1621960803` is the timestamp when the build was done.

```bash
#
# Example docker.conf
#
IMAGE_NAME=tamarack

#
# Evolene tags docker images using https://semver.org/ notation, major.minor.path.
#
# IMAGE_VERSION=major.minor
# The Patch is normally added by Evolene at build time using the current timestamp.
#

IMAGE_VERSION=2.3

#
# You can override using $BUILD_NUMBER as patch number for SemVer by
# explicitly adding it aswell.
# If this was set, the result whould be tamarack:2.3.0_f2486d7
#
# PATCH_VERSION=0

```

# Testing

If you have 🔑 secret environment variables somewhere in your tests, add them in your Github repository `/ Settings / Secrets / Repository secrets / EVOLENE_TEST_SECRETS` as _key=value_ pairs and access them as `$(YOUR_ENV_KEY)` or as envs i Docker Compose files.

EVOLENE_TEST_SECRETS can be either a oneliner or separate rows.

```bash
# EVOLENE_TEST_SECRETS example
API_KEY=abc123
DB_PWD=123abc
```

```yaml
    environment:
      - DB_URL="https://example.com:1234"
      - DB_USER="admin"
      - DB_PWD
      - API_KEY
```
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
      - ${WORKSPACE}/tests:/tests
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

# Docker Registries

The default regisry is a private registry, but if you would like to publish your Docker image to the public Docker Hub, this can be done by setting env `PUSH_PUBLIC` to `true`. This will push your image to `hub.docker.com/r/kthse`.

Your built image will get two tags will get, the ususual SemVer with commit `tamarack:2.3.40_f2486d7`, but also and also a short tag with only SemVer `tamarack:2.3.40`. This is done to enable reuse of tags.

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

# Send build arguments to the docker build

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

The default behaiour is that only main branch (master or main) will be pushed to NPM or Docker registries. Other branches will build and tested, but not saved to a artifact storage like Docker Hub.

## Save long lived branches to repository

```bash
BRANCHES_SAVE_STARTING_WITH="origin/feature-"
```

If you would like to use and save a branch other then main to a repository, you kan force Evolene to save the artifact by setting env `BRANCHES_SAVE_STARTING_WITH` on the branch build job on the CI server, and thereby overriding the default behaivour. This will save the built image (docker push). Note that the version will include the branch name.

**Example:** If you build _my-project_ with version _2.3.2_ on a branch named _origin/a-feature-branch-a_ and have env `BRANCHES_SAVE_STARTING_WITH="origin/feature-"`, the result will be that `my-project:origin.a.feature.branch.a-2.3.2_abcdefg` is save to the repository.

This will also make every other branch starting with "origin/feature-" to have its artifact saved.

### Tag long lived branches as main (enable semver update)

```bash
BRANCHES_SAVE_STARTING_WITH="origin/parallell-rewrite"
BRANCHES_TAG_AS_MAIN="True"
```

If you need continuous delivery based on semver updates in Aspen for a long lived branch. You can set env `BRANCHES_TAG_AS_MAIN="True"` together with BRANCHES_SAVE_STARTING_WITH. This will change the standard version behaviour for none-main branches and remove the branch name in the version. So instead of creating `my-project:origin.parallell.rewite-4.5.6_f23t56`, the result will look like its the branch was a main build `my-project:4.5.6_f23t56`.

**Note:** This may cause version collisions if you save image from multiple branches to the same reposity.
