# Useful functions for working with AWS parameter store
import boto3

from ksp_deploy.config import ENABLE_SSL, AWS_REGION

def get_ssm_value(param_name):
    """Gets the value of an encrypted parameter from the AWS SSM"""
    client = boto3.client('ssm', verify=ENABLE_SSL, region_name=AWS_REGION)
    try:
        return client.get_parameter(Name=param_name, WithDecryption=True)["Parameter"]["Value"]
    except KeyError:
        print("Couldn't find parameter")
