# Takes specific pre-deploy actions after builds have completed, like tagging
import os
import subprocess
from argparse import ArgumentParser

from ksp_deploy.credentials import find_credentials
from ksp_deploy.helpers import get_build_data, get_version_file_info, get_version
from ksp_deploy.config import KSPConfiguration
from ksp_deploy.logging import set_logging


def tag(mod_data_file):
    """
    Tag the repo if needed.

    Inputs:
        mod_data_file (str): path to mod data yaml (defaults to the one in ksp_deploy.config.py)

    """

    # Create/load the config
    config = KSPConfiguration()

    if mod_data_file == "":
        mod_data_file = config.BUILD_DATA_NAME
    build_data = get_build_data(mod_data_file)
    version_data = get_version_file_info(os.path.join(os.path.dirname(mod_data_file), "GameData", build_data['mod-name']), build_data['mod-name'])

    version = get_version(version_data)

    logger.info(f"Tagging {build_data['mod-name']} version {version}")

    repo_slug = os.environ["GITHUB_REPOSITORY"]
    github_user = find_credentials("GITHUB_USER", config)
    github_user_email = find_credentials("GITHUB_USER_EMAIL", config)
    github_token = find_credentials("OAUTH_TOKEN", config)

    tag_test_cmd = f"git tag -l {version}"
    output = subprocess.check_output(tag_test_cmd, shell=True)
    if version in str(output):
        logger.info(f"Tag {version} already exists, skipping tagging")
    else:
        logger.info(f"Tagging repo with {version}")
        auth_cmd = f"git config --local user.name '{github_user}' && git config --local user.email '{github_user_email}' && git remote rm origin && git remote add origin https://{github_user}:{github_token}@github.com/{repo_slug}.git"
        tag_cmd = f"git tag {version}"
        push_cmd = f"git push origin {version}"

        subprocess.check_output(auth_cmd, shell=True)
        subprocess.check_output(tag_cmd, shell=True)
        subprocess.check_output(push_cmd, shell=True)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", default="",
                        help="custom package data file path")

    args = parser.parse_args()

    logger = set_logging("staging")
    tag(args.file)
