# # from flask_mail import Message
# # from extension import mail
# import resend
# from config import Config
# def send_verification_email(email, fullname, verification_link):

#     resend_api_key = Config.RESEND_API_KEY
#     param = {
#                 "from": "onboarding@resend.dev",
#                 "to": email,
#                 "subject": "Verify Email",
#                 "html": f"""
#                         Hello {fullname},
                        
#                         Thank you for registering.
                        
#                         Click the link to verify your email.
#                         {verification_link}
#                     """
#             }
#     resend.Emails.send(param)
 
from brevo import Brevo
from config import Config
from flask import current_app
from brevo.transactional_emails import (SendTransacEmailRequestSender, SendTransacEmailRequestToItem)

def send_verification_email(email, subject, html):
    client = Brevo(
        api_key=current_app.config("BREVO_API_KEY")
    )
    client.transactional_emails.send_transac_email(
    subject=subject,
    html_content=html,
    sender=SendTransacEmailRequestSender(
        name=current_app.config("MAIL_FROM_TITLE"),
        email=current_app.config("MAIL_FROM")
    ),
    to={
        SendTransacEmailRequestToItem(
            email=email
        )
    }
    )
