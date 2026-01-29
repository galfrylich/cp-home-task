import os
import time
import json
import boto3
from datetime import datetime

AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
S3_BUCKET = os.getenv("S3_BUCKET")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))

sqs = boto3.client("sqs", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)


def upload_to_s3(payload: dict):
    now = datetime.utcnow()
    key = (
        f"emails/"
        f"{now.year}/{now.month:02d}/{now.day:02d}/"
        f"{int(time.time() * 1000)}.json"
    )

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(payload),
        ContentType="application/json"
    )

    print(f"Uploaded to s3://{S3_BUCKET}/{key}")


while True:
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])

    if not messages:
        print("No messages in queue")
        time.sleep(POLL_INTERVAL)
        continue

    for msg in messages:
        try:
            body = json.loads(msg["Body"])
            upload_to_s3(body)

            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

            print("Message processed and deleted")

        except Exception as e:
            print("Error processing message:", e)
            # message will reappear after visibility timeout
