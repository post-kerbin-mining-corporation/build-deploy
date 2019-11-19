# Getting Started

To get started using this pack, you will need to do a bit of setup.

1. **Collect credentials:** first go through all the logins and passwords you will need
2. **Setup credentials**: configure these credentials so they can be used with the workflow
3. **Setup Travis-CI**: important setup options for Travis-CI
4. **Setup your repository**: how to lay out and configure your repository for deployment
5. **Configure the deployment**: Configure the deployment

## 1. Collect Credentials
These scripts require a number of credentials which you should collect before getting started. **DO NOT STORE THESE ON YOUR REPO ANYWHERE.** 

### GitHub

You will need your GitHub credentials regardless of where you want to deploy. This includes your email, username and an Oauth token (generate this [here](https://github.com/settings/tokens))

### CurseForge

If you want to deploy your mod to CurseForge, you will need a **CurseForge API token**. Follow their instructions [here](https://authors.curseforge.com/account/api-tokens) to generate one.

### SpaceDock

If you want to deploy your mod to SpaceDock, you will need your SpaceDock **login** and **password**.

### AWS

If you want to deploy your mod to S3, download dependencies from S3, or use the AWS ParameterStore implementation to store all the above credentials, you will need an AWS IAM user with the appropriate permissions (correct bucket read/write, ParameterStore read). YOu will need that account's **access key** and **secret**.


## 2. Setup Credentials

Credentials need to be set up so the deploy scripts can access them. There are currently two options - Travis encrypted environment variables and AWS Parameter Store. 

### AWS ParameterStore

The default provider for credentials is AWS Parameter Store. If the flag `USE_SSM_CREDENTIALS` is set to `True` in the 
`.ksp_deploy_config.yml` file, the package will go and fetch credentials from AWS ParameterStore. This is handy because there is no need to individually input all the above credentials in every repo you use.

In the AWS console or CLI, you will set the following parameters (though you can use less if not deploying to SpaceDock or CurseForge):

* `ksp-spacedock-login`: Spacedock user login
* `ksp-spacedock-password`: SpaceDock password
* `ksp-curseforge-token`: Curseforge generated token
* `ksp-github-user`: Github user name
* `ksp-github-user-email`: Github user email
* `ksp-github-oauth-token`: Github Oauth generated token

The AWS credentials to access ParameterStore are specified as encrypted environment variables in Travis-CI. These credentials should have read access to ParameterStore, and read/write access to the S3 buckets you want. Specifically you should set up these two variables in Travis-CI:
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`


### Environment Variables
If you don't want to use AWS to store credentials, set `USE_SSM_CREDENTIALS` to `False` in the `.ksp_deploy_config.yml` file. If you do this you will need to provide the relevant environment variables, set up as encrypted parameters for the repo in the Travis CI console or CLI. You need to set the following:
* `SPACEDOCK_LOGIN`
* `SPACEDOCK_PASSWORD`
* `CURSEFORGE_TOKEN`
* `GITHUB_USER`
* `GITHUB_USER_EMAIL`
* `GITHUB_OAUTH_TOKEN`

You will need to do this for every repo you set up.

## 3. Travis-CI Setup

Enable Travis-CI on your repo by going through the GitHub Marketplace.

### Settings

Go to the Travis-CI panel for your repo (at eg. https://travis-ci.com/YourGithubName/YourRepoName/settings) and configure these switches:

* Build Pushed Branches: On
* Build Pushed Pull Requests:  On
* Limit Concurrent Jobs: Off
* Auto Cancel Branch Builds: On
* Auto Cancel Pull Request Builds: On

### Environment Variables

Setup the required environment variables as indicated above - if using AWS ParameterStore, you only need to set up:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY` 

If not, add:
* `SPACEDOCK_LOGIN`
* `SPACEDOCK_PASSWORD`
* `CURSEFORGE_TOKEN`
* `GITHUB_USER`
* `GITHUB_USER_EMAIL`
* `GITHUB_OAUTH_TOKEN`



## 4. Repository Setup
First, copy `.travis.yml` and `.mod_data.yml` to the root of your repository (remove the `.example`). You can optionally copy `.ksp_deploy_config.yml` if you want to customize more options. 

This package expects that your repository be laid out like this:

```
* root
  * GameData                     // Typically, things you will deploy will be here
    * ModNameHere
      * Versioning
        * ModNameHere.version   // A version file is needed
  * source_code                 // Typically source is not inside GameData
  * assets                      // Typically source is not inside GameData
  * readme.txt                  // optional but nice
  * changelog.txt               // Changelogs are generated from this file
  * .travis.yml
  * .mod_data.yml
  * .ksp_deploy_config.yml      // Optional
```

## 5. Configure Deployment

