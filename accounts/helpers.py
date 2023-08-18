import resend
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User
from . import emails

# TODO: Use Django send_email SMTP in production
# TODO: Change domain of URL message in production

# def send_forgot_email(email: str, token: str, uidb64: str) -> bool:
#     """Send email to user with link to reset password

#     Args:
#         email (str): User email
#         token (str): Temporary token to reset password
#         uidb64 (str): Base 64 encode of user id

#     Returns:
#         bool: True
#     """

#     subject = 'Link to recover password'
#     message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/forgot-my-password/{uidb64}/{token}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)

#     return True


def send_confirmation_email(email: str, name: str, token: str, uidb64: str) -> bool:
    """Send an email to user with link to confirm email using Resend API and test domain (Change in production)

    Args:
        email (str): Non active user email
        Name (str): Non active user full name
        token (str): Temporary token to confirm the email
        uidb64 (str): Base 64 encode of user id

    Returns:
        bool: True
    """

    resend.api_key = settings.RESEND_API_KEY
    params = emails.confirmation_email(email, name, token, uidb64)
    resend.Emails.send(params)

    return True


def send_forgot_email(email: str, token: str, uidb64: str) -> bool:
    """Send email to user with link to reset password using Resend API and test domain (Change in production)

    Args:
        email (str): User email
        token (str): Temporary token to reset password
        uidb64 (str): Base 64 encode of user id

    Returns:
        bool: True
    """

    resend.api_key = settings.RESEND_API_KEY
    params = emails.forgot_email(email, token, uidb64)
    resend.Emails.send(params)

    return True


def send_contact_support_email(sender_email: str, sender_name: str, subject: str, email_body: str) -> bool:
    """Send email to our contact email using Resend API and test domain (Change in production)

    Args:
        sender_email (str): Sender email
        subject (str): Subject of the email
        email_body (str): Text of the email

    Returns:
        bool: True
    """

    resend.api_key = settings.RESEND_API_KEY
    params = emails.contact_support_email(sender_email, sender_name, subject, email_body)
    resend.Emails.send(params)

    return True


def get_tokens_for_user(user: User | None) -> dict[str, str]:
    """
    Create refresh and access token with email

    Args:
        user (User): Minerva Database user

    Returns:
        tokens (dict): Refresh token and access token.
    """

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.email + str(timestamp) +
            str(user.is_active)
        )


confirmation_token_generator = CustomTokenGenerator()
