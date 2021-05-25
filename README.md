# 🐳 Evolene CI ![Continous Integration](https://github.com/KTH/kth-azure-app/actions/workflows/main.yml/badge.svg)

**Evolene CI runs a sequence of steps that build, test and in the end stores a Docker or NPM package in a registry. It is KTH:s way of standardising the build process so that developers never have to learn about anything about continuous integration systems 😃 or having to care where built artefacts are stored.**

Utilizing Docker and Docker Compose everyting that a developer runs on her laptop is run the same way in the CI environment. No need for setting up a build or integration test environment on an external service. The idea is that a developer does a `git push` when it works locally, and Evolene handles the rest.

Evolene uses Convention Over Configuration. That means that Evolene is configured by following standard naming convensions rather then per project configuration.

## How to use Evolene CI as a developer

- [🐳 Common configuration available for both Docker and NPM](https://github.com/KTH/evolene/blob/master/README-DOCKER.md)
- [🐳 How to build, test and publish your Docker application](https://github.com/KTH/evolene/blob/master/README-DOCKER.md)
- [📦 How to build, test and publish your NPM application](https://github.com/KTH/evolene/blob/master/README-NPM.md)
