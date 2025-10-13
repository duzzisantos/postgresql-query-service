import smtplib, ssl
from email import encoders, errors
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from io import BytesIO


async def dispatch_email(mail_server: str, subject: str, body: str, sender_email: str, receiver_email: str | list[str], password: str, attachment: BytesIO):
    
   try:
       ## Create multipart message with headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email ## if bulk recipients

    message.attach(MIMEText(body, "plain"))
    filename = attachment

  
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.getvalue())

    
    ## Encode part as ASCII
    encoders.encode_base64(part)

    part.add_header(
        "Content_Disposition",
        f"attachment; filename= {filename}"
    )

    ## Add attachment to message - convert to string
    message.attach(part)
    text= message.as_string()

   ## Context for SSL
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(mail_server, 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

   except errors.InvalidBase64CharactersDefect:
      raise HTTPException(status_code=422, detail="Email is not properly formatted")
   except errors.CharsetError:
      raise HTTPException(status_code=422, detail="Email contains illegal or unacceptable character(s) in its caracter set")
   except errors.HeaderDefect:
      raise HTTPException(status_code=422, detail="There's been an email header defect. Check attachment and try again")
   except errors.MessageError:
      raise HTTPException(status_code=500, detail="Internal Server Error")
   

    



    