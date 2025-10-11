from utils.email_template import dispatch_email
from pydantic import BaseModel
from typing import Any

class SendQueryFileToEmail:
    def __init__(self, recipient, sender, password, role, subject, message, email_server, attachment):
        self.recipient = recipient
        self.sender = sender
        self.password = password
        self.role = role
        self.subject = subject
        self.message = message
        self.email_server = email_server
        self.attachment= attachment

    def validate_email_content(self):
            if(self.role.__eq__("")):
                return {"Message": "You must specify user role", "Status": False}
            elif(self.role and (item.__eq__("") or len(item) == 0) for item in [self.recipient, self.sender, self.password, self.message, 
                                                                                self.role, self.subject, self.email_server, self.attachment]):
                return {"Message": "All email content must be fully provided", "Status": False}
            else:
                return {"Message": "Successful validation", "Status": True}


     
    async def send_to_recipients(self):
            validate = self.validate_email_content()
            if validate["Status"] == True:
                 return await dispatch_email(self.email_server, self.subject, self.message, self.sender, self.recipient, self.password, self.attachment)
            else:
                 return validate

    ## Add any other email template

        



class EmailProperties(BaseModel):
     recipient: str | list[str]
     sender: str
     password: str
     role: str | list[str]
     subject: str
     message: str
     email_server: str
     attachment: str | Any        