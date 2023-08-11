from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

# TODO: Change domain of URL message
def send_forgot_email(email: str, token: str, uidb64: str) -> bool:
    """Send email to user with link to reset password

    Args:
        email (str): User email
        token (str): Temporary token to reset password
        uidb64 (str): Base 64 encode of user id

    Returns:
        bool: True
    """

    subject = 'Link to recover password'
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/change-password/{uidb64}/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

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