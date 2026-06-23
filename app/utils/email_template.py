import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from io import BytesIO
from app.core.config import settings


def dispatch_email(
    subject: str,
    body: str,
    sender_email: str,
    receiver_email: str | list[str],
    password: str,
    attachment: BytesIO = None,
    attachment_filename: str = "report.xlsx",
    mail_server: str = None,
    mail_port: int = None,
    use_tls: bool = None,
):
    """
    Send an email with optional attachment. Plug-and-play with any SMTP provider:
    - Gmail: smtp.gmail.com, port 587, TLS
    - Outlook: smtp.office365.com, port 587, TLS
    - Amazon SES: email-smtp.us-east-1.amazonaws.com, port 587, TLS
    - Direct SSL (port 465) is auto-detected when use_tls=False and port=465.

    Falls back to SMTP_* env vars for any omitted parameter.
    """
    server_host = mail_server or settings.SMTP_HOST
    server_port = mail_port or settings.SMTP_PORT
    tls = use_tls if use_tls is not None else settings.SMTP_USE_TLS
    sender = sender_email or settings.SMTP_USER
    pwd = password or settings.SMTP_PASSWORD

    if not server_host:
        raise HTTPException(status_code=422, detail="No SMTP server configured. Set SMTP_HOST or pass email_server.")
    if not sender or not pwd:
        raise HTTPException(status_code=422, detail="Sender email and password are required.")

    recipients = receiver_email if isinstance(receiver_email, list) else [receiver_email]

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if attachment is not None:
        attachment.seek(0)
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_filename}")
        message.attach(part)

    try:
        context = ssl.create_default_context()

        if not tls and server_port == 465:
            # Direct SSL connection (legacy providers)
            with smtplib.SMTP_SSL(server_host, server_port, context=context, timeout=30) as srv:
                srv.login(sender, pwd)
                srv.sendmail(sender, recipients, message.as_string())
        else:
            # STARTTLS — the modern default (port 587 or 25)
            with smtplib.SMTP(server_host, server_port, timeout=30) as srv:
                srv.ehlo()
                if tls:
                    srv.starttls(context=context)
                    srv.ehlo()
                srv.login(sender, pwd)
                srv.sendmail(sender, recipients, message.as_string())

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="SMTP authentication failed. Check sender/password.")
    except smtplib.SMTPConnectError:
        raise HTTPException(status_code=503, detail=f"Could not connect to SMTP server {server_host}:{server_port}")
    except smtplib.SMTPRecipientsRefused:
        raise HTTPException(status_code=422, detail="One or more recipient addresses were rejected by the server.")
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected email error: {str(e)}")
