# Takes specific pre-deploy actions after builds have completed, like tagging
import os
import subprocess
from ksp_deploy.authentication import get_ssm_value


from ksp_deploy.config import SSMKeys

def tag(version):
    """
    Tag the repo if needed.

    Inputs:
        version (str): tag to create

    """
    repo_slug = os.environ["TRAVIS_REPO_SLUG"]
    github_user = get_ssm_value(SSMKeys.GITHUB_USER)
    github_user_email = get_ssm_value(SSMKeys.GITHUB_USER_EMAIL)
    github_token = get_ssm_value(SSMKeys.GITHUB_OAUTH_TOKEN)

    tag_test_cmd = f"git tag -l {version}"
    output = subprocess.check_output(tag_test_cmd, shell=True)
    if (version in output):
        logger.info(f"Tag {version} already exists, skipping tagging")
    else:
        logger.info(f"Tagging repo with {version}")
        auth_cmd = f"git config --local user.name '{github_user}' && - git config --local user.email '{github_user_email}' &&  set-url origin https://{github_user}:{github_token}@github.com/{repo_slug}.git"
        tag_cmd = f"git tag {version}"
        push_cmd = f"git push origin {version}"

        subprocess.check_output(auth_cmd, shell=True)
        subprocess.check_output(tag_cmd, shell=True)
        subprocess.check_output(push_cmd, shell=True)

if __name__ == "__main__":

    logger = set_logging("staging")
    tag()
