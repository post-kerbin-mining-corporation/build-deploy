This repository presents a set of python scripts that can be used to package Kerbal Space Program mods and deploy them to typical locations, in this case S3, GitHub, CurseForge and SpaceDock
# Usage
If you want to use these and you're not me, well, you can give it a shot with this guide.
## AWS Setup
These scripts rely on access to AWS Parameter Store (storing credentials) and AWS S3 (storing built packages for distribution and dependencies). TO get set up, you should create an IAM user with an appropriate policy to read/upload from S3, and read from ParameterStore.

Infrastructure-wise, you will need:
1. An S3 bucket with dependencies that you are using.
2. A second S3 bucket to deploy to, if desired
3. ParameterStore keys with appropriate credentials for your deploy targets

You can see/change the names of the ParameterStore keys in `ksp_deploy.config.py`

## Travis-CI Setup
These scripts run through Travis CI, so you should enable that for your repository. You also need to set two encrypted environment variables through the web interface or CLI for the IAM user you're using. These authorize access to the AWS account and are used for accessing S3 and ParameterStore. Ensure you follow Travis best practices for storing these.
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

## Repository Setup
First, copy `.travis.yml` and `.mod_data.yml` to the root of your repository (remove the `.example`). Next, set up your mod data by configuring these files.

### `.mod_data.yml`
This file stores mod-specific information about deployment. Here you specify your dependencies for packaging and your deploy targets

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
      mod-id: 230112  # The CurseForge mod ID for deployment
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
