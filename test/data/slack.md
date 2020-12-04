```
Sending build context to Docker daemon  17.17MB
Step 1/22 : FROM kthse/kth-nodejs:14.0.0
14.0.0: Pulling from kthse/kth-nodejs
Digest: sha256:3b9a82de2b9bd0a96acc178751fbfdba9dc0b9c7741b196a5cb432fbb2c87d6f
Status: Image is up to date for kthse/kth-nodejs:14.0.0
---> b7283b8bf5d9
Step 2/22 : RUN mkdir -p /npm &&     mkdir -p /application
---> Using cache
---> 02e39361cb50
Step 3/22 : WORKDIR /npm
---> Using cache
---> c43d53eee4eb
Step 4/22 : COPY ['package.json', 'package.json']
---> bf70234ffcf0
Step 5/22 : COPY ['package-lock.json', 'package-lock.json']
---> b980d3791414
Step 6/22 : RUN npm install --production --no-optional
---> Running in 1228108896e4
sharp@0.23.4 install /npm/node_modules/sharp
(node install/libvips && node install/dll-copy && prebuild-install) || (node-gyp rebuild && node install/dll-copy)
[91minfo[0m[91m sharp Downloading https://github.com/lovell/sharp-libvips/releases/download/v8.8.1/libvips-8.8.1-linuxmusl-x64.tar.gz
[0m[91mprebuild-install WARN install No prebuilt binaries found (target=14.15.1 runtime=node arch=x64 libc=musl platform=linux)
[0m[91mgyp ERR! find Python
gyp ERR! find Python Python is not set from command line or npm configuration
gyp ERR! find Python Python is not set from environment variable PYTHON
gyp ERR! find Python checking if 'python' can be used
gyp ERR! find Python - 'python' is not in PATH or produced an error
gyp ERR! find Python checking if 'python2' can be used
gyp ERR! find Python - 'python2' is not in PATH or produced an error
gyp ERR! find Python checking if 'python3' can be used
gyp ERR! find Python - 'python3' is not in PATH or produced an error
gyp ERR! find Python
gyp ERR! find Python **********************************************************
gyp ERR! find Python You need to install the latest version of Python.
gyp ERR! find Python Node-gyp should be able to find and use Python. If not,
gyp[0m[91m ERR! find Python you can try one of the following options:
gyp ERR! find Python - Use the switch --python='/path/to/pythonexecutable'
gyp ERR! find Python   (accepted by both node-gyp and npm)
gyp ERR! find Python - Set the environment variable PYTHON
gyp ERR! find Python - Set the npm configuration variable python:
gyp ERR! find Python   npm config set python '/path/to/pythonexecutable'
gyp ERR! find Python For more information consult the documentation at:
gyp ERR! find Python https://github.com/nodejs/node-gyp#installation
gyp ERR! find Python **********************************************************
gyp ERR! find Python
[0m[91mgyp ERR! configure error
[0m[91mgyp ERR! stack Error: Could not find any Python installation to use
gyp ERR! stack     at PythonFinder.fail (/usr/local/lib/node_modules/npm/node_modules/node-gyp/lib/find-python.js:307:47)
gyp ERR! stack     at PythonFinder.runChecks (/usr/local/lib/node_modules/npm/node_modules/node-gyp/lib/find-python.js:136:21)
gyp ERR! stack     at PythonFinder.<anonymous> (/usr/local/lib/node_modules/npm/node_modules/node-gyp/lib/find-python.js:179:16)
gyp ERR! stack     at PythonFinder.execFileCallback (/usr/local/lib/node_modules/npm/node_modules/node-gyp/lib/find-python.js:271:16)
gyp ERR! stack     at exithandler (child_process.js:315:5)
gyp ERR! stack     at ChildProcess.errorhandler (child_process.js:327:5)
gyp ERR! stack     at ChildProcess.emit (events.js:315:20)
gyp ERR! stack     at Process.ChildProcess._handle.onexit (internal/child_process.js:275:12)
gyp ERR! stack     at onErrorNT (internal/child_process.js:465:16)
gyp ERR! stack     at processTicksAndRejections (internal/process/task_queues.js:80:21)
[0m[91mgyp ERR! System Linux 3.10.0-1127.19.1.el7.x86_64
[0m[91mgyp ERR! command '/usr/local/bin/node' '/usr/local/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js' 'rebuild'
[0m[91mgyp ERR! cwd /npm/node_modules/sharp
09:53
gyp[0m[91m ERR! node -v v14.15.1
[0m[91mgyp ERR! node-gyp -v v5.1.0
gyp ERR![0m[91m not ok
[0m[91mnpm ERR! code ELIFECYCLE
npm ERR! errno 1
[0m[91mnpm ERR! sharp@0.23.4 install: (node install/libvips && node install/dll-copy && prebuild-install) || (node-gyp rebuild && node install/dll-copy)
npm ERR! Exit status 1
npm ERR!
npm ERR! Failed at the sharp@0.23.4 install script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output above.
[0m[91m
npm ERR! A complete log of this run can be found in:
npm ERR!     /root/.npm/_logs/2020-11-27T08_53_19_646Z-debug.log
[0mThe command '/bin/sh -c npm install --production --no-optional' returned a non-zero code: 1
```