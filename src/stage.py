# Takes specific pre-deploy actions after builds have completed, like tagging
import os
import subprocess
from authentication import get_ssm_value


def tag(version):
    """
    Tag the repo if needed.

    Inputs:
        version (str): tag to create

    """
    repo_slug = os.environ["TRAVIS_REPO_SLUG"]
    github_user = get_ssm_value("ksp-github-user")
    github_user_email = get_ssm_value("ksp-github-user-email")
    github_token = get_ssm_value("ksp-github-oauth-token")

    tag_test_cmd = f"git tag -l {version}"
    output = subprocess.check_output(tag_test_cmd, shell=True)
    if (version in output):
        logger.info(f"Tag {version} already exists, skipping tagging")
    else:
        logger.info(f"Tagging repo with {version}")
        auth_cmd = f"git config --local user.name '{github_user}' && - git config --local user.email '{github_user_email}' &&  set-url origin https://{github_user}:{github_token}@github.com/{repo_slug}.git"
        tag_cmd = "git tag {version}"
        push_cmd "git push origin {version}"

if __name__ == "__main__":

    logger = set_logging("staging")
    tag()
