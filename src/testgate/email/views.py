# from sqlmodel import Session
# from fastapi import APIRouter, Depends
#
# import src.testgate.user.service as auth_service
# from src.testgate.user.models import User
# from src.testgate.user.views import retrieve_current_user
# from config import get_settings, Settings
#
# from src.testgate.email.service import EmailService, get_email_service
# from src.testgate.database.service import get_session

# email_router = APIRouter(tags=["emails"])


# @email_router.post(
#     path="/api/v1/emails/verification", response_model=None, status_code=200
# )
# def send_verification_email(
#     *,
#     session: Session = Depends(get_session),
#     settings: Settings = Depends(get_settings),
#     email_service: EmailService = Depends(get_email_service),
# ):
#     email_service.email_subject = "Email Verification"
#     email_service.email_to = "user.email"
#     email_service.add_plain_text_message(
#         "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
#     )
#     email_service.add_html_message(
#         """\
#             <html>
#                 <head></head>
#                 <body>
#                     <p>
#                         Hi!
#                         <br>How are you?<br>
#                         Here is the <a href="http://www.python.org">link</a> you wanted.
#                     </p>
#                 </body>
#             </html>
#         """
#     )
#     email_service.send_email()

# email_service = EmailService()
# email_service.email_subject = "Email Verification"
# email_service.email_from = SMTP_EMAIL_ADDRESS
# email_service.email_to = user.email
# email_service.email_password = SMTP_EMAIL_APP_PASSWORD
#
# email_service.add_plain_text_message("Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org")
# email_service.add_html_message(
#     """\
#         <html>
#             <head></head>
#             <body>
#                 <p>
#                     Hi!
#                     <br>How are you?<br>
#                     Here is the <a href="http://www.python.org">link</a> you wanted.
#                 </p>
#             </body>
#         </html>
#     """)
# email_service.send_email()
