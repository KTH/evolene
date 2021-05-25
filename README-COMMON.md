# Configuration envs available for Docker and NPM pipelines

## Build information to file

If you would like to get build information writen to a file. Set `BUILD_INFORMATION_OUTPUT_FILE` to a relative path
in your repo. Depending on the file extension a different file type will be created. (overwritten if it already exists).

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/version.js'
```

### Different file types

#### HTML

```bash
BUILD_INFORMATION_OUTPUT_FILE='/config/version.html'
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

# Get Slack notifications where new NPM package are available

If you set NPM*UPDATES_AVAILABLE to true. Evolene will inform you about
packages in you \_package.json* that have updates. It makes it easier to
keep your dependencies up to date and hopefully make your code easier
to maintain, since this helps changes come in smaller increments.
Evolene always outputs this informatin in the build log, even if you
choose not to see it in Slack.

`NPM_UPDATES_AVAILABLE=True`

# Slack channels to post build information to

Comma separated list of channels to post messages to. Messages are build inforation,
failures an push information.

```bash
SLACK_CHANNELS='#pipeline-logs,#devops'
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

### Feature flag for building

Sometimes we add new features that are sort of in beta. If you would like to try these out allow
exprimental.

```bash
EXPERIMENTAL='True' # Set or unset
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
