import boto3


def get_service_client(service):
    return boto3.client(
        service,
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID
    )


def get_s3_client():
    return get_service_client(service="s3")


def get_dynamo_client():
    return get_service_client(service="dynamo")

def get_cloudwatch_client():
    return get_service_client(service='cloudwatch')

def get_dynamo_table(table_id: str):
    resource = boto3.resource('dynamodb')

    return resource.Table(table_id)
