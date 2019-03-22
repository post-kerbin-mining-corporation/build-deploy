import os
import shutil
import zipfile
import zlib
import logging
from urllib.parse import urlparse
import shutil
import requests

import ksp_deploy.aws.s3 as s3

logger = logging.getLogger('packager.dependencies')


def download_dependency(name, info, temp_path, build_path, config):
    """
    Downloads a dependency record from either S3 (external dependency) or github (internal dependency)

    Inputs:
        name (str): name of the dependency
        info (dict): dictionary describing the dependency
        temp_path (str): path to store dependency zips to
        build_path (str): path to stage to
        config (KSPConfiguration): config
    """
    if info["location"] == "s3":
        logger.info(f"Collecting {name} {info['version']} from S3")
        download_dependency_s3(name, info["version"], temp_path, build_path, config)

    if info["location"] == "github":
        logger.info(f"Collecting {name} at tag {info['tag']} from repository {info['repository']}")
        download_dependency_github(name, info['repository'], info["tag"], temp_path, build_path, config)

    if info["location"] == "url":
        logger.info(f"Collecting {name} at from {info['url']}")
        download_dependency_url(name, info['url'], temp_path, build_path, config, zip=info.get("zip", False))

def download_dependency_s3(name, version, temp_path, build_path, config):
    """
    Downloads and unzips a dependency from S3

    Inputs:
        name (str): name of the dependency
        bucket (str): S3 bucket to pull from
        version (str): version of the dependency
        temp_path (str): path to store dependency zips to
        build_path (str): path to stage to
        config (KSPConfiguration): config
    """
    target_name = os.path.join(temp_path, f"{name}_{version}.zip")
    logger.info(f"Pulling s3://{config.DEPENDENCY_BUCKET}/external/{name}_{version}.zip")
    s3.copy(f"s3://{config.DEPENDENCY_BUCKET}/external/{name}_{version}.zip", target_name)

    with zipfile.ZipFile(target_name, "r") as z:
        z.extractall(build_path)

def download_dependency_url(name, url, temp_path, build_path, config, zip=True):
    """
    Downloads a dependency from a url

    Inputs:
        name (str): name of the dependency
        url (str): url of the dependency
        temp_path (str): path to store dependency zips to
        build_path (str): path to stage to
        zip (bool): is the target file a zip of standard format?
        config (KSPConfiguration): config
    """
    parsed = urlparse(url)
    fn = os.path.basename(parsed.path)
    target_name = os.path.join(temp_path, fn)
    logger.info(f"Downloading {url} to {target_name}")

    download_file(url, target_name)

    if zip:
        with zipfile.ZipFile(target_name, "r") as z:
            z.extractall(build_path)
    else:
        shutil.copy(target_name, os.path.join(build_path, "GameData"))

def download_dependency_github(name, repo, tag, temp_path, build_path, config):
    """
    Downloads a github repo with a specific tag

    Inputs:
        name (str): name of the dependency
        repo (str): Account/RepoName
        tag (str): version of the dependency (tagged in the repo)
        temp_path (str): path to store dependency zips to
        build_path (str): path to stage to
        config (KSPConfiguration): config
    """
    wp = os.getcwd()
    os.chdir(temp_path)
    # Clone into the repo, pull the specified tag
    clone_cmd = f"git clone https://github.com/{repo}.git"
    tag_cmd = f"git checkout master && git fetch && git fetch --tags && git checkout {tag}"
    os.system(clone_cmd)
    os.chdir(name)
    os.system(tag_cmd)
    os.chdir(wp)
    # Move the contents of GameData into the build directory
    shutil.copytree(os.path.join(temp_path, name, "GameData", name), os.path.join(build_path, "GameData", name))


def download_file(url, local_filename):
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    return local_filename
