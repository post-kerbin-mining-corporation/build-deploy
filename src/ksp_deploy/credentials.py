import os
from ksp_deploy.aws.ssm import get_ssm_value


def find_credentials(credential_name, config):
    """
    Finds a credential item, either from AWS SSM or from environment variables

    Inputs:
        credential_name (string): the name of the credential to fetch
        config (KSPConfiguration): instance of config class
    Returns:
        credential_value (string): the value of the credential
    """
    try:
        if config.USE_SSM_CREDENTIALS:
            return get_ssm_value(config.CRED_NAME_TO_KEYS[credential_name], config.ENABLE_SSL, config.AWS_REGION)
        else:
            return os.environ[credential_name]
    except:
        print(f"Error fetching {credential_name}")
