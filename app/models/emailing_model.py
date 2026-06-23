from app.utils.email_template import dispatch_email
from io import BytesIO


class SendQueryFileToEmail:
    def __init__(self, recipient, sender, password, role, subject, message,
                 email_server=None, email_port=None, use_tls=None,
                 attachment: BytesIO = None, attachment_filename: str = "report.xlsx"):
        self.recipient = recipient
        self.sender = sender
        self.password = password
        self.role = role
        self.subject = subject
        self.message = message
        self.email_server = email_server
        self.email_port = email_port
        self.use_tls = use_tls
        self.attachment = attachment
        self.attachment_filename = attachment_filename

    def validate(self) -> dict:
        if not self.recipient:
            return {"Message": "Recipient is required", "Status": False}
        if not self.subject or not self.message:
            return {"Message": "Subject and message body are required", "Status": False}
        return {"Message": "Validation passed", "Status": True}

    def send(self):
        """Synchronous send — safe to call from Celery tasks."""
        validation = self.validate()
        if not validation["Status"]:
            return validation

        dispatch_email(
            subject=self.subject,
            body=self.message,
            sender_email=self.sender,
            receiver_email=self.recipient,
            password=self.password,
            attachment=self.attachment,
            attachment_filename=self.attachment_filename,
            mail_server=self.email_server,
            mail_port=self.email_port,
            use_tls=self.use_tls,
        )
        return {"Message": "Email sent successfully", "Status": True}
