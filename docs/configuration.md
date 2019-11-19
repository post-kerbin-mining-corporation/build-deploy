# Configuration

There are four configuration files that should be edited to configure the mod:

* `.mod_data.yml`: Customize mod information
* `GameData/ModNameHere/Versioning/ModNameHere.version`: Customize the mod version
* `.travis.yml`: Customize the deployment scripts
* `.ksp_deploy_config.yml`: Customize advanced options

## `.mod_data.yml`
This file stores mod-specific information about how to deploy. Here you specify your dependencies for packaging and your deploy targets.
It is broken down into a few sections

### mod-name

This is the name of your mod, which should match the folder name in GameData. Zips will be named according to this as well.

### package

This controls the packaging of the mod

* `include-dependencies`: whether to package the dependencies as well
* `included-gamedata`: if you have multiple GameData-level items in your distribution, specify them here
* `included-support`: if you have multiple root-level items in your distribution, specify them here. This could be things like changelogs, license files, etc

### dependencies**

This section specifies dependenceis to bundle with the mod. 

A dependency block starts with the name of the dependency.
```
CryoTanks:
  location: s3
  version: 2.6.0  
```
 The most important field is the `location` item, which specifies where to fetch this dependency from. There are three possible values:

`s3`
This specifies that the dependency should be pulled from S3. It will be pulled from the S3 bucket specified in `.ksp_deploy_config.yml`. These items should be zipped with a structure that looks like `GameData/Dependency/Stuff` You should also specify:
* `version`: A string that will be appended to the mod name to collect the appropriate zip file, eg `CryoTanks_2.6.0.zip`

`github`
This specifies that the dependency should be a repository cloned from Github with a specific tag. These dependencies should have a root level `GameData` folder containing the dependency. You should also specify:
* `repository`: The org and name of the repo, eg 'ChrisAdderley/CryoTanks'
* `tag`: The tag that should be collected. Make sure to check that the tag exists.

`url`
This specifies that the dependency is pulled from a simple URL. This can either be a zipfile, like the S3 one described above, or a simple flat single file (eg. a dll). You should also specify:
* `url`: The URL of the file
* `zip`: True if this is a zip, packaged as `GameData/Dependency/Stuff`

### deploy

This section provides a list of deploy targets. Each can be enabled or disabled by changing the `enabled` flag. Currently 3 are supported.

`SpaceDock`
Deploy to Spacedock. You must supply a `mod-id` which is the numeric ID, as indicated in the SpaceDock URL. You must ensure the SpaceDock credentials are setup correctly (see [Getting Started](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/start.md))
`CurseForge`
Deploy to Curseforge. You must supply a `mod-id` which is the numeric ID of the project, as shown on the mod's webpage. You must provide the CurseForge-generated Oauth token (see [Getting Started](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/start.md))
`GitHub`
Deploy to GitHub releases. You must supply appropriate GitHub user information (see [Getting Started](https://github.com/post-kerbin-mining-corporation/build-deploy/blob/master/docs/start.md))

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


## `ModNameHere.version`

This is a standard .version file of the AVC specification. It is compatible with KSP-AVC and MiniAVC. The deploy scripts in this package use this to determine what the version of your mod is, as well as what versions of KSP it is compatible with. Here are the important parameters

`NAME`

This should match the name in the `.mod_data.yml` file.

`VERSION`

Make sure this block is incremented every time you release. It is used to tell the deploy providers what version your mod is and generate the filename for the zip. 

`KSP_VERSION`

This tells the providers what KSP version this was built for. If it was built for 1.6.1, put that here. It will be entered on SpaceDock, Curse, etc

Example file.
```
{
    "NAME":"ModNameHere",
    "URL":"https://raw.githubusercontent.com/ChrisAdderley/CryoEngines/master/GameData/CryoEngines/Versioning/CryoEngines.version",
    "DOWNLOAD":"http://forum.kerbalspaceprogram.com/threads/117766",
    "VERSION":
    {
        "MAJOR":0,
        "MINOR":6,
        "PATCH":5,
        "BUILD":0
    },
    "KSP_VERSION":
    {
        "MAJOR":1,
        "MINOR":6,
        "PATCH":1
    },
    "KSP_VERSION_MIN":{
        "MAJOR":1,
        "MINOR":6,
        "PATCH":0
    },
    "KSP_VERSION_MAX":{
        "MAJOR":1,
        "MINOR":6,
        "PATCH":99
    }
}
```

## `.travis.yml`

You shouldn't need to change this much unless using S3 deploys. Check the commented lines for possible pitfalls
```
# Example travis script for using these build and deploy scripts
language: python
python:
  - 3.6
install:
  - pip install awscli boto3 requests
branches:
  only:
    - master                                                                     # Change this if your release branch is not master
script:
  - git clone https://github.com/post-kerbin-mining-corporation/build-deploy.git  
  - git checkout tags/1.0.0                                                     # change 1.0.0 to use a different version of these scripts
  - python src/package.py  # Run the package script
  - cd ..
  - pytest -s --testpath "GameData/" build-deploy/src/tests/  
  - python build-deploy/src/package.py --f ".mod_data.yml"  
before_deploy:
  - python build-deploy/src/stage.py --f ".mod_data.yml"
deploy:
   - provider: script
    script: python build-deploy/src/deploy.py --f ".mod_data.yml"              # Deploy  package to spacedock, curse, github
    skip_cleanup: true
    on:
      branch: master                                                           # Change this if your release branch is not master
  - provider: s3                                                               # Releases to S3. Remove this block if not using
    access_key_id: $AWS_ACCESS_KEY_ID
    secret_access_key: $AWS_SECRET_ACCESS_KEY
    bucket: "nertea-ksp-modding-releases"                                      # Change this to your target bucket
    local_dir: deploy/ReStock                                                  # Change ReStock to your mod name
    skip_cleanup: true
    acl: public_read
    region: us-east-2
    upload-dir: restock                                                        # Change this to the prefix you want for your mod
    on:
      branch: master                                                           # Change this if your release branch is not master
```

## `.ksp_deploy_config.yml`

This file allows you to customize some elements of the package. Each setting is optional. 

* `TEMP_PATH`: local temp path. defaults to `tmp`. Avoid changing.
* `BUILD_PATH`: local temp path. defaults to `build`. Avoid changing.
* `DEPLOY_PATH`: local temp path. defaults to `deploy`. Avoid changing.
* `BUILD_DATA_NAME`: name of the mod data file. Defaults to  `.mod_data.yml`
* `CHANGELOG_PATH`: name of the changelog, defaults to `changelog.txt`
* `DEPENDENCY_BUCKET`: name of the S3 bucket to pull `s3` type dependencies from. Defaults to `nertea-ksp-modding-dependencies`
* `AWS_REGION`: AWS region to use, defaults to `us-east-2`
* `ENABLE_SSL`: Keep `True`
* `USE_SSM_CREDENTIALS`: Whether to use AWS Parameter Store to get secrets. If False, uses local environment variables. Defaults to `True`
