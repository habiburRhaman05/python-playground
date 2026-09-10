from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from pathlib import Path
class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "devhabib2005@gmail.com",
    MAIL_PASSWORD = "wtub reei aqbj swkz",
    MAIL_FROM = "devhabib2005@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Habib",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
     TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates'
)


async def send_mail(payload,sub):
    print(payload)
    context_data ={
        "body": {
        "name": payload['name'],
        "company": "AI Technologies"
    }
    }
    message = MessageSchema(
        subject=sub,
        recipients=[payload["email"]],
        template_body=context_data,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message,template_name='welcome_email.html')
    print("sended")
    return {"message": "email has been sent"}