from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from jose import jwt, JWTError
import boto3
import json

from app.schemas import RequestPayload
from app.config import get_jwt_secret, SQS_QUEUE_URL, AWS_REGION

app = FastAPI(title="Email API Service")

sqs = boto3.client("sqs", region_name=AWS_REGION)
JWT_SECRET = get_jwt_secret()
JWT_ALGORITHM = "HS256"


def verify_token(token: str):
    expected = JWT_SECRET.strip()
    received = token.strip()

    if received != expected:
        print(f"DEBUG token mismatch: received='{received}' expected='{expected}'")
        raise HTTPException(status_code=401, detail="Invalid token")

def validate_timestamp(ts: str):
    if not ts.isdigit():
        raise HTTPException(
            status_code=400,
            detail="email_timestream must be a Unix timestamp"
        )

    try:
        datetime.utcfromtimestamp(int(ts))
    except (ValueError, OSError):
        raise HTTPException(
            status_code=400,
            detail="email_timestream is not a valid timestamp"
        )

@app.post("/send")
def send_message(
    payload: RequestPayload,
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ")[1]
    verify_token(token)

    validate_timestamp(payload.data.email_timestream)
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(payload.dict())
    )

    return {
        "status": "sent",
        "message_id": response["MessageId"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

