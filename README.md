This repository presents a set of Python scripts that can be used to package Kerbal Space Program mods and deploy them to typical user download locations, in this case S3, GitHub, CurseForge and SpaceDock. It uses Travis-CI to do this.
# Usage
If you want to use these and you're not me, well, you can give it a shot with this guide. If you are using them, please let me know so I can refactor/clea things up.

## Credentials
These scripts require a set of credentials for the various deploy providers that are used. There are currently two options for this.
### AWS
The default provider for credentials is AWS Parameter Store. If the flag `USE_SSM_CREDENTIALS` is set to `True` in the `.ksp_deploy_config.yml` file, the package will go and fetch credentials from AWS ParameterStore. The AWS credentials to do this retrieval are used from local environment variables that should be set up as encrypted parameters for the repo in the Travis CI console or CLI. These credentials should have read access to ParameterStore, and read/write access to the S3 buckets you want. Specifically you should set:
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

You can also set up any of the other AWS CLI options such as region in this way. These are the same parameters that Travis will use to deploy to S3.

The parameters you need to set are as follows, though you can get away with less if not using the spacedock or CurseForge deployers.
* `ksp-spacedock-login`: Spacedock user login
* `ksp-spacedock-password`: SpaceDock password
* `ksp-curseforge-token`: Curseforge generated token
* `ksp-github-user`: Github user name
* `ksp-github-user-email`: Github user email
* `ksp-github-oauth-token`: Github Oauth generated token

### Environment Variables
If you don't want to use AWS to store credentials, set `USE_SSM_CREDENTIALS` to `False` in the `.ksp_deploy_config.yml` file. If you do this you will need to provide the relevant environment variables, likely set up as encrypted parameters for the repo in the Travis CI console or CLI. You need to set the following:
* `SPACEDOCK_LOGIN`
* `SPACEDOCK_PASSWORD`
* `CURSEFORGE_TOKEN`
* `GITHUB_USER`
* `GITHUB_USER_EMAIL`
* `GITHUB_OAUTH_TOKEN`

## Configuration
How to set things up.
## AWS Setup
If using AWS, you should set up AWS Parameter Store and AWS S3 (storing built packages for distribution and dependencies). To get set up, you should create an IAM user with an appropriate policy to read/upload from S3, and read from ParameterStore.

Infrastructure-wise, you will need:
1. An S3 bucket with dependencies that you are using.
2. A second S3 bucket to deploy to, if desired
3. ParameterStore keys with appropriate credentials for your deploy targets (see Credentials section above)

## Travis-CI Setup
Enable Travis-CI on your repo.

## Repository Setup
First, copy `.travis.yml` and `.mod_data.yml` to the root of your repository (remove the `.example`). You can optionally copy `.ksp_deploy_config.yml` if you want to customize paths and options. Next, set up your mod data by configuring these files.

#### `.ksp_deploy_config.yml`

This file allows you to customize some elements of the package. Each setting is optional. 

* `TEMP_PATH`: local temp path. defaults to `tmp`
* `BUILD_PATH`: local temp path. defaults to `build`
* `DEPLOY_PATH`: local temp path. defaults to `deploy`
* `BUILD_DATA_NAME`: name of the mod data file. Defaults to  `.mod_data.yml`
* `CHANGELOG_PATH`: name of the changelog, defaults to `changelog.txt`
* `DEPENDENCY_BUCKET`: name of the S3 bucket to pull `s3` type dependencies from. Defaults to `nertea-ksp-modding-dependencies`
* `AWS_REGION`: AWS region to use, defaults to `us-east-2`
* `ENABLE_SSL`: Keep `True`
* `USE_SSM_CREDENTIALS`: Whether to use AWS Parameter Store to get secrets. If False, uses local environment variables. Defaults to `True`

#### `.mod_data.yml`
This file stores mod-specific information about how to deploy. Here you specify your dependencies for packaging and your deploy targets. Though the file is mostly clear, there are some gotchas

**package**

* `included-gamedata`: if you have multiple GameData-level items in your distribution, specify them here
* `included-support`: if you have multiple root-level items in your distribution, specify them here

**dependencies**

A dependency block starts with the name of the dependency.
```
CryoTanks:
  location: s3
  version: 2.6.0  
```
 The most important field is the `location` item, which specifies where to fetch this dependency from. There are three possible values:

`s3`
This specifies that the dependency should be pulled from S3. It will be pulled from the bucket specified in `.ksp_deploy_config.yml`. These items should be zipped with a structure that looks like `GameData/Dependency/Stuff` You should also specify:
* `version`: A string that will be appended to the mod name to collect the appropriate zip file, eg `CryoTanks_2.6.0.zip`

`github`
This specifies that the dependency should be a repository cloned from Github. Generally these dependencies should have a root level `GameData` folder containing the dependency. You should also specify:
* `repository`: The org and name of the repo
* `tag`: The tag that should be collected

`url`
This specifies that the dependency is pulled from a simple URL. This can either be a zipfile, like the S3 one described above, or a simple flat single file (eg. a dll). You should also specify:
* `url`: The URL of the file
* `zip`: True if this is a standard dependency zip

#### deploy

This scetion provides a list of deploy targets. Each can be enabled or disabled by changing the `enabled` flag. Currently 3 are supported.

`SpaceDock`
Deploy to Spacedock. You must supply a `mod-id` which is the numeric ID. You must provide the user Id and password of an authorized project contributor via environment variable sor via ParameterStore (see Credentials section)
`CurseForge`
Deploy to Curseforge. You must supply a `mod-id` which is the numeric ID of the project. You must provide the CurseForge-generated Oauth token either via environment variable or via ParameterStore (see Credentials section)
`GitHub`
Deploy to GitHub releases. You must supply appropriate GitHub user information via environment variables or via ParameterStore (see Credentials section)

```
# Example annotated build data file
mod-name: ModNameHere  # Name of the mod's GameData directory
package:
  included-gamedata  # Include these gamedata-level folders in packages:
    - ReStock
  included-support:  # Include these root-level files in packages
    - readme.txt
    - changelog.txt
    - LICENSE
dependencies:  # Configure dependencies
  B9PartSwitch:
    version: 2.6.0  # The version to use
    location: s3  # Pull this from an S3 location
  CryoTanks:
    location: github  # Pull this from a github repo
    repository: ChrisAdderley/CryoTanks  # Repository slug
    tag: 1.1.1  # The release tag to use
deploy:
  - SpaceDock:
      enabled: false  # activate/deactivate this deployment script
      mod-id: 709  # The Spacedock mod ID for deployment
  - CurseForge:
      enabled: false  # activate/deactivate this deployment script
      mod-id: 230112  # The CurseForge mod ID for deployment
  - GitHub:
      enabled: false  # activate/deactivate this deployment script
```

### `.travis.yml`

You shouldn't need to change this much. Just ensure the `bucket` and `upload-dir` lines align with what you want in your s3 bucket.
```
# Example travis script for using these build and deploy scripts
language: python
python:
  - 3.6
install:
  - pip install awscli boto3 requests
branches:
  only:
    - master # only run me on merges to master
script:
  - git clone https://github.com/post-kerbin-mining-corporation/build-deploy.git  # clone this repo
  - git checkout master # change this to run off a different CI repo branch
  - python src/package.py  # Run the package script
before_deploy:
  - python stage.py  # Run the staging script
deploy:
  - provider: script
    script: python src/build_scripts/deploy.py
    skip_cleanup: true
    on:
      condition: $TRAVIS_BRANCH = master
  - provider: s3 # releases to S3
    access_key_id: $AWS_ACCESS_KEY_ID
    secret_access_key: $AWS_SECRET_ACCESS_KEY
    bucket: "nertea-ksp-modding-releases"
    local_dir: deploy
    skip_cleanup: true
    acl: public_read
    region: us-east-2
    upload-dir: cryo-engines
    on:
      condition: $TRAVIS_BRANCH = master
```
