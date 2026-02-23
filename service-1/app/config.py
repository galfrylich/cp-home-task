import os
import boto3

AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "dev-email-queue")

SSM_PARAM_NAME = os.getenv(
    "JWT_SSM_PARAM",
    "/dev/email-service/jwt-secret",
)


def get_jwt_secret():
    ssm = boto3.client("ssm", region_name=AWS_REGION)
    param = ssm.get_parameter(
        Name=SSM_PARAM_NAME,
        WithDecryption=True,
    )
    return param["Parameter"]["Value"]
