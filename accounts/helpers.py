from django.core.mail import send_mail
import uuid
from django.conf import settings


def send_forgot_email(email: str, token: str, uidb64: str) -> bool:
    subject = 'Link to recover password'
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/password-reset/{uidb64}/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
