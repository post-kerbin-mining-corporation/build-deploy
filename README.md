This repository presents a workflow that can be used to automatically package Kerbal Space Program mods and deploy them to typical user download locations, in this case S3, GitHub, CurseForge and SpaceDock. 

# Overview

The overall concept of this workflow is as follows:

1. The project is deemed ready for release by the author
2. A pull request is created from the current development branch to the release branch (`master` by default)
3. Travis-CI runs packaging and deployment tests on the target
4. Success or failure is reported
4. Merging the pull request triggers Travis-CI to run automated tagging of the repo, packaging of binaries, and uploading of the binaries to target deployment repositories.

# Requirements

You need the following things to use this package

* A repository structure that mimics this example
* Travis-CI set up on the repository
* A bit of work configuring thing

# Documentation

Please review to get started

1. [Getting Started](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/start.md)
2. [Configuration](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/configuration.md)
3. [Changelogs and more](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/misc.md)
4. [Tests](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/tests.md)

# Problems

Problems or issues? Let me know by creating an issue. 