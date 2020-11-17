import os
import yaml


class KSPConfiguration:

    class __KSPConfiguration:
        # Paths
        TEMP_PATH = "tmp"
        BUILD_PATH = "build"
        DEPLOY_PATH = "deploy"
        BUILD_DATA_NAME = ".mod_data.yml"  # default path of the build data file
        CHANGELOG_PATH = "changelog.txt"  # name of the changelog file

        # AWS stuff
        DEPENDENCY_BUCKET = "nertea-ksp-modding-dependencies"  # where to look for dependencies
        AWS_REGION = "us-east-2"
        ENABLE_SSL = True
        USE_SSM_CREDENTIALS = True

        # Mapping of credential names to SSM keys
        CRED_NAME_TO_KEYS = {
                "SPACEDOCK_LOGIN": "ksp-spacedock-login",
                "SPACEDOCK_PASSWORD": "ksp-spacedock-password",
                "CURSEFORGE_TOKEN": "ksp-curseforge-token",
                "GITHUB_USER": "ksp-github-user",
                "GITHUB_USER_EMAIL": "ksp-github-user-email",
                "OAUTH_TOKEN": "ksp-github-oauth-token"
            }
        def __init__(self, config_path):
            self._load_yaml_config(config_path)

        def __str__(self):
            return repr(self) + self.val

        def _load_yaml_config(self, config_path):
            config_data = {}
            try:
                with open(config_path, "r") as f:
                  config_data = yaml.load(f)
            except IOError:
                print ("No .deploy_config.yml file was found, defaults will be used")

            self.TEMP_PATH = config_data.get("TEMP_PATH", "tmp")
            self.BUILD_PATH = config_data.get("BUILD_PATH", "build")
            self.DEPLOY_PATH = config_data.get("DEPLOY_PATH", "deploy")
            self.BUILD_DATA_NAME = config_data.get("BUILD_DATA_NAME", ".mod_data.yml")
            self.CHANGELOG_PATH = config_data.get("CHANGELOG_PATH", "changelog.txt")
            self.DEPENDENCY_BUCKET = config_data.get("DEPENDENCY_BUCKET", "nertea-ksp-modding-dependencies")
            self.AWS_REGION = config_data.get("AWS_REGION", "us-east-2")
            self.ENABLE_SSL = config_data.get("ENABLE_SSL", True)
            self.USE_SSM_CREDENTIALS = config_data.get("USE_SSM_CREDENTIALS", True)

    instance = None

    def __init__(self, config_path=".ksp_deploy_config.yml"):
        if not KSPConfiguration.instance:
            KSPConfiguration.instance = KSPConfiguration.__KSPConfiguration(config_path)

    def __getattr__(self, name):
        return getattr(self.instance, name)
