from app.utils.email_template import dispatch_email
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
            elif(self.recipient.__eq__("") or self.sender.__eq__("") or self.password.__eq__("") or self.message.__eq__("") or 
                                                                                self.role.__eq__("") or  self.subject.__eq__("") or self.email_server.__eq__("") ):
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

