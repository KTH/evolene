# 📦 NPM Pipeline Configuration

Besides from working with Docker images, Evolene also supports building and publishing NPM packages.

## NPM pipeline requirements

- `/npm.conf` This file needs to contain the _node version_ to build the packet with.

## Publish NPM packages

1. **Add a `/npm.conf` file** in the root of your repo. This file needs to contain the _node version_ to build the packet with.

```bash

# What version of node should be used?
NODE_VERSION=14

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

## Automaticly publish all builds

You can configure your npm packages to publish to npm registy on every commit. This is done by adding a `"automaticPublish": "true"` in the root of the **package.json**. This will make Evolene look in the npm registry for the latest published version that matches "major.minor" and incrementing the patch version by one.

```json
{
  "version": "1.0.2",
  "automaticPublish": "true"
}
```

Example: If you have version: 1.0.2, Evolene will look for the latest version 1.0, in this example 1.0.9. Increment patch version to 10, and push 1.0.10.

![Published package are shown in Slack](https://github.com/KTH/evolene/blob/master/images/npm.png)

## Build information added to NPM packages automatically

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

# Get Slack notifications where new NPM package are available

If you set NPM_UPDATES_AVAILABLE to true. Evolene will inform you about
packages in you `package.json` that have updates. It makes it easier to
keep your dependencies up to date and hopefully make your code easier
to maintain, since this helps changes come in smaller increments.
Evolene always outputs this informatin in the build log, even if you
choose not to see it in Slack.

`NPM_UPDATES_AVAILABLE=True`
