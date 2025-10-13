from pydantic import BaseModel
from typing import Optional, Any


class EmailProperties(BaseModel):
     recipient: Optional[str | list[str]]
     sender: str
     password: str
     role: Optional[str | list[str]]
     subject: str
     message: str
     email_server: str