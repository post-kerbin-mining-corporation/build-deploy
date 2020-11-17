# Deploy script entrypoint
import os
import shutil
import zipfile
import zlib
import requests
from argparse import ArgumentParser

from ksp_deploy.config import KSPConfiguration
from ksp_deploy.credentials import find_credentials

from ksp_deploy.logging import set_logging
from ksp_deploy.helpers import get_build_data, get_version_file_info, get_changelog, get_version, get_ksp_version
from ksp_deploy.spacedock import SpaceDockAPI
from ksp_deploy.curseforge import CurseForgeAPI
from ksp_deploy.github import GitHubReleasesAPI


def deploy(mod_data_file):
    """
    Deploys packages to providers

    Inputs:
        mod_data_file (str): path to mod data yaml (defaults to the one in ksp_deploy.config.py)
    """
    # Create/load the config
    config = KSPConfiguration()

    # Collect build information
    if mod_data_file == "":
        mod_data_file = config.BUILD_DATA_NAME
    build_data = get_build_data(mod_data_file)
    version_data = get_version_file_info(os.path.join(os.path.dirname(mod_data_file), "GameData", build_data['mod-name']), build_data['mod-name'])

    changelog = get_changelog(os.path.join(os.path.dirname(mod_data_file), config.CHANGELOG_PATH))

    logger.info(f"Deploying {build_data['mod-name']} version {get_version(version_data)}\n=================")
    logger.info(f"Changes:\n{changelog}")

    zipfile = os.path.join("deploy", build_data['mod-name'], f"{build_data['mod-name']}_" + "{MAJOR}_{MINOR}_{PATCH}.zip".format(**version_data["VERSION"]))
    logger.info(f"Deploying {zipfile}")

    if "SpaceDock" in build_data["deploy"] and build_data["deploy"]["SpaceDock"]["enabled"]:
        deploy_spacedock(
            get_version(version_data),
            get_ksp_version(version_data),
            build_data["deploy"]["SpaceDock"]['mod-id'],
            changelog,
            zipfile,
            config)
    if "CurseForge" in build_data["deploy"] and build_data["deploy"]["CurseForge"]["enabled"]:
        deploy_curseforge(
            get_ksp_version(version_data),
            build_data["deploy"]["CurseForge"]['mod-id'],
            changelog,
            zipfile,
            config)

    if "GitHub" in build_data["deploy"] and build_data["deploy"]["GitHub"]["enabled"]:
        deploy_github(
            get_version(version_data),
            changelog,
            zipfile,
            config)

def deploy_curseforge(ksp_version, mod_id, changelog, zipfile, config):
    """
    Performs deployment to CurseForge

    Inputs:
        ksp_version (str): version of KSP to target
        mod_id (str): CurseForge project ID
        changelog (str): Markdown formatted changelog
        zipfile (str): path to file to upload
        config (KSPConfiguration): configuration instance
    """
    logger.info("Deploying to CurseForge")

    curse_token = find_credentials("CURSEFORGE_TOKEN", config)

    with CurseForgeAPI(curse_token) as api:
        api.update_mod(mod_id, changelog, ksp_version, "release", zipfile)

def deploy_spacedock(version, ksp_version, mod_id, changelog, zipfile, config):
    """
    Performs deployment to SpaceDock

    Inputs:
        version (str): mod version
        ksp_version (str): version of KSP to target
        mod_id (str): CurseForge project ID
        changelog (str): Markdown formatted changelog
        zipfile (str): path to file to upload
        config (KSPConfiguration): configuration instance
    """

    spacedock_user = find_credentials("SPACEDOCK_LOGIN", config)
    spacedock_pw = find_credentials("SPACEDOCK_PASSWORD", config)

    logger.info(f"Deploying {zipfile} to SpaceDock project {mod_id}")
    try:
        with SpaceDockAPI(spacedock_user, spacedock_pw) as api:
            if api.check_version_exists(mod_id, version):
                logger.warning("Skipping Spacedock deploy as version already exists")
            else:
                api.update_mod(mod_id, version, changelog, ksp_version, True, zipfile)
    except requests.exceptions.ConnectionError as err:
        logger.warning(f"Skipping Spacedock deploy as Spacedock is down ({err})")

def deploy_github(version, changelog, zipfile, config):
    """
    Performs deployment to GitHub releases

    Inputs:
        version (str): mod version
        changelog (str): Markdown formatted changelog
        zipfile (str): path to file to upload
        config (KSPConfiguration): configuration instance
    """
    logger.info("Deploying to GitHub Releases")

    github_user = find_credentials("GITHUB_USER", config)
    github_token = find_credentials("GITHUB_OAUTH_TOKEN", config)
    repo_slug = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ["GITHUB_REF"]

    with GitHubReleasesAPI(github_user, github_token, repo_slug) as api:

        latest = api.get_latest_release()

        try:
            latest_name = latest.get("name", "")
            logger.info(f"Latest release was {latest_name}")
        except AttributeError:
            logger.info(f"No previous releases")
            latest_name = ""

        slug = os.environ["GITHUB_REPOSITORY"]
        owner, repo = slug.split('/')
        if latest_name == f"{repo} {version}":
            latest_id = latest["id"]
            assets = api.get_release_assets(latest_id)
            if len(assets) == 0:
                logger.warning("Release already exists but has no assets, zip will be uploaded")
                do_upload = True
                release_id = latest["id"]
            else:
                do_upload = True
                release_id = latest["id"]
                for asset in assets:
                    if asset["name"] == os.path.basename(zipfile):
                        logger.warning(f"Skipping GitHub deploy as version and file {asset['name']} ({os.path.basename(zipfile)}) already exist")
                        do_upload = False
                if do_upload:
                    logger.warning(f"Release already exists but has a missing asset, {zipfile} will be uploaded")
        else:
            logger.info(f"Creating new release for version {version} on branch {branch}")
            response = api.create_release(version, changelog, branch)
            release_id = response["id"]
            do_upload = True

        if do_upload:
            logger.info(f"Uploading {zipfile} to GitHub")
            api.upload_release_file(release_id, zipfile)
        else:
            logger.warning("Skipping file upload as version already exists")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", default="",
                        help="custom package data file path")

    args = parser.parse_args()
    logger = set_logging("deployment")
    deploy(args.file)
