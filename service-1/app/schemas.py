from pydantic import BaseModel
from pydantic import ConfigDict

class EmailData(BaseModel):
    email_subject: str
    email_sender: str
    email_timestream: str
    email_content: str

    model_config = ConfigDict(extra="forbid")

class RequestPayload(BaseModel):
    data: EmailData
