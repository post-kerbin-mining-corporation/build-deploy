import boto3

def get_ssm_value(param_name, ssl=True, region="us-east-2"):
    """Gets the value of an encrypted parameter from the AWS SSM"""
    client = boto3.client('ssm', verify=ssl, region_name=region)
    try:
        return client.get_parameter(Name=param_name, WithDecryption=True)["Parameter"]["Value"]
    except KeyError:
        print("Couldn't find parameter")
