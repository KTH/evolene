# Evolene CI ![Continous Integration](https://github.com/KTH/evolene/actions/workflows/main.yml/badge.svg)

**Evolene CI runs a sequence of steps that build, test and in the end stores a Docker or NPM package in a registry. It is our way of standardising the build process, so that developers never have to learn anything about our continuous integration systems 😃 or having to care where built artefacts are stored, or what processes to follow. Every user of Evolene run the same steps and when we add new features, everyone gets them without having to do anything 🍾**

The main principle for Evolene is  everything that a developer runs on her laptop is run the same way in the CI environment. No need for setting up a build or integration test environment on an external service. The idea is that a developer does a `git push` when it works locally, and Evolene handles the rest.

Evolene uses Convention Over Configuration. That means that Evolene is configured by following standard naming convensions rather then per project configuration. The Slack integration helps the developers if any configuration is missing or test breaks.

## Use Evolene CI with Github Actions

Add this to a Github Action workflow `.github/workflows`. That is it 🎉! 

If you have 🔑 secret environment variables somewhere in your process (like tests) add them in `/ Settings / Secrets / Repository secrets / EVOLENE_TEST_SECRETS` as _key=value_ pairs and access them as `$(YOUR_ENV_KEY)`, there are more customizing you can do:

- [🛠️ Common Docker and NPM](https://github.com/KTH/evolene/blob/master/README-DOCKER.md)
- [🐳 How to build, test and publish your Docker application](https://github.com/KTH/evolene/blob/master/README-DOCKER.md)
- [📦 How to build, test and publish your NPM application](https://github.com/KTH/evolene/blob/master/README-NPM.md)

```yaml
name: Evolene CI

on:
  push:
    branches: [master]
  workflow_dispatch:

jobs:
  Evolene:
    name: Continuous Integration
    runs-on: ubuntu-20.04
    steps:
      - uses: actions/checkout@v2.3.4
      - name: Build, Test and Push with Evolene
        run: |
          SLACK_CHANNELS=#team-developers \
          BUILD_INFORMATION_OUTPUT_FILE='/version.conf' \
          EVOLENE_TEST_SECRETS=${{secrets.EVOLENE_TEST_SECRETS}} \
          
          ${{ secrets.EVOLENE_RUN_COMMAND }}
```

### Need a good looking badge?
Add ![Continous Integration](https://github.com/KTH/evolene/actions/workflows/main.yml/badge.svg) `![Continous Integration](https://github.com/KTH/YOUR-REPO_NAME/actions/workflows/main.yml/badge.svg)` to your _README.md_ ;)
