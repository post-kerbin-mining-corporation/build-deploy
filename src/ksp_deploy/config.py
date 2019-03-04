
# Paths
TEMP_PATH = "tmp"
BUILD_PATH = "build"
DEPLOY_PATH = "deploy"
BUILD_DATA_NAME = ".mod_data.yml"  # default path of the build data file
CHANGELOG_PATH = "changelog.txt"  # name of the changelog file
DEPENDENCY_BUCKET = "nertea-ksp-modding-dependencies"  # where to look for dependencies

AWS_REGION = "us-east-2"
ENABLE_SSL = True

class SSMKeys:
    SPACEDOCK_LOGIN = "ksp-spacedock-login"
    SPACEDOCK_PASSWORD = "ksp-spacedock-password"
    CURSEFORGE_TOKEN = "ksp-curseforge-token"
    GITHUB_USER = "ksp-github-user"
    GITHUB_USER_EMAIL = "ksp-github-user-email"
    GITHUB_OAUTH_TOKEN = "ksp-github-oauth-token"

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
