import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_email(subject, body):

    email_address = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not email_address or not app_password:

        raise ValueError(
            "Email credentials are missing from .env"
        )

    message = EmailMessage()

    message["From"] = email_address
    message["To"] = email_address
    message["Subject"] = subject

    message.set_content(body)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            email_address,
            app_password
        )

        smtp.send_message(message)

    print(
        "\nEmail sent successfully."
    )