from pydantic import BaseModel
from typing import Optional


class EmailProperties(BaseModel):
    recipient: Optional[str | list[str]] = None
    sender: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str | list[str]] = None
    subject: str
    message: str
    # SMTP config — falls back to env vars when omitted
    email_server: Optional[str] = None
    email_port: Optional[int] = None
    use_tls: Optional[bool] = None
