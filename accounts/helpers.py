import resend
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from .models import User

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
#     message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/password-reset/{uidb64}/{token}'
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

    params = {
        "from": f"MinervaLMS <{settings.RESEND_DOMAIN}>",
        "to": email,
        "subject": "MinervaLMS - Confirm your email",
        "html": f"""
        <p>Dear {name},<br>
        Welcome to MinervaLMS! We're thrilled to have you as part of our learning community. To ensure the security of your account and provide you with a seamless experience, we kindly ask you to confirm your email address.</p>

        <p>Please click on the link below to verify your email:</p>
        <a href="http://frontend-two-rosy.vercel.app/confirm-email/{uidb64}/{token}">
        http://frontend-two-rosy.vercel.app/confirm-email/{uidb64}/{token}</a>

        <p>If you didn't sign up for MinervaLMS or have received this email by mistake, please disregard it.
        Thank you for choosing MinervaLMS for your educational journey. </p>

        <The>Best regards,<br>
        The MinervaLMS Team</p>
        """,
    }

    email = resend.Emails.send(params)

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

    params = {
        "from": f"MinervaLMS <{settings.RESEND_DOMAIN}>",
        "to": email,
        "subject": "MinervaLMS - Link to recover your password",
        "html": f"""
        <p>We hope this email finds you well. It appears that you have requested a password reset for your MinervaLMS account. If you did not make this request, please ignore this message.</p>

        <p>If you did request a password reset, please use the following link to reset your password:</p>
        <a href="http://frontend-two-rosy.vercel.app/password-reset/{uidb64}/{token}">
        http://frontend-two-rosy.vercel.app/password-reset/{uidb64}/{token}</a>

        <p>Thank you for using MinervaLMS.</p>

        <The>Best regards,<br>
        The MinervaLMS Team</p>
        """,
    }

    email = resend.Emails.send(params)

    return True


def send_contact_email(sender_email: str, sender_name: str, subject: str, email_body: str) -> bool:
    """Send email to our contact email using Resend API and test domain (Change in production)

    Args:
        sender_email (str): Sender email
        subject (str): Subject of the email
        email_body (str): Text of the email

    Returns:
        bool: True
    """

    resend.api_key = settings.RESEND_API_KEY
    ticket_id = int(datetime.now().timestamp() * 1000)

    params = {
        "from": f"MinervaLMS <{settings.RESEND_DOMAIN}>",
        "to": settings.SUPPORT_EMAIL,
        "cc": sender_email,
        "subject": f"MinervaLMS Support - Ticket #{ticket_id}",
        "html": f"""
        <p>Dear {sender_name},<br>
        <p>Thank you for getting in touch with our support team. We appreciate the opportunity to assist you.<br>
        Here is the text of your inquiry:</p>

        <p><i><b>Subject:</b> {subject}<br>
        "{email_body}"</i></p>

        <p>Our team is already hard at work investigating your issue and finding the best possible solution. We understand how important this matter is to you, and we are committed to resolving it promptly.</p>

        <The>Best regards,<br>
        The MinervaLMS Team</p>
        """,
    }

    email = resend.Emails.send(params)

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