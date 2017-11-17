# Evolene - Standradized building on Jenkins

Jenkins build as code.

Features:
* Verifies **docker.conf**
* Verifies **Dockerfile**
* Repo security scanning for passwords and secrets
* Docker build
* SemVer versioning of Docker images
* Push to Docker Registry
* Slack integration for build information
* Contarinerized integration testing by running **docker-compose-integration-tests.yml**	
* Contarinerized unit testing by running **docker-compose-unit-tests.yml**

## How to use on Jenkins
Do use Evolene on Jenkins simply [add a build step](https://build.sys.kth.se/view/team-pipeline/job/kth-azure-app/configure) that executes run.sh. Evolene uses Convention Over Configuration. That means that Evolene is configure by following standard naming convensions rather then per project configuration.

![KTH on Azure](https://gita.sys.kth.se/Infosys/evolene/blob/master/images/jenkins.png)

Default configuration
```bash
SLACK_CHANNELS="#team-studadm-build" $EVOLENE_DIRECTORY/run.sh
```

Latest feature:
```bash
SLACK_CHANNELS="#team-studadm-build,#pipeline-logs" DEBUG=True EXPERIMENTAL=True $EVOLENE_DIRECTORY/run.sh
```


# How to develop and run Evolene on your local machine

To run: 
```bash
python run.py docker run-pipeline
```

To create dist:
```bash
./create_dist.sh
```
The version of the dist is defined in `setup.py`

To run tests:
```bash
./run_tests.sh
```

All environment variables for configuration:

```
IMAGE_NAME          - The name of the image to build (ex: 'kth-azure-app')
PROJECT_ROOT        - The path to the root of the project to build (ex: '/Users/projects/kth-azure-app')
GIT_COMMIT          - The commit hash of the push that triggered the build (usually set by Jenkins)
BUILD_NUMBER        - The number of the current build (usually set by Jenkins)
SLACK_WEB_HOOK      - The Slack webhook endpoint to use
SLACK_CHANNELS      - Comma separated list of channels to post messages to (ex: '#pipeline-logs,#zermatt')
REGISTRY_HOST       - The host (without protocol) of the Docker registry to use (ex: 'kthregistryv2.sys.kth.se')
REGISTRY_USER       - Registry user
REGISTRY_PASSWORD   - Registry password
EVOLENE_DIRECTORY   - The working directory of evolene (used on jenkins to work properly)
EXPERIMENTAL        - Feature toogle for latest features
```

Changes to this project are automatically sent to https://build.sys.kth.se

