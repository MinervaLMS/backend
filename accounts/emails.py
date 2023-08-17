from datetime import datetime
from django.conf import settings


def confirmation_email(email: str, name: str, token: str, uidb64: str) -> dict:
    return {
        "from": f"MinervaLMS <{settings.RESEND_DOMAIN}>",
        "to": email,
        "subject": "MinervaLMS - Confirm your email",
        "html": f"""
        <p>Dear {name},<br>
        Welcome to MinervaLMS! We're thrilled to have you as part of our learning community. To ensure the security of your account and provide you with a seamless experience, we kindly ask you to confirm your email address.</p>

        <p>Please click on the link below to verify your email:</p>
        <a href="http://frontend-two-rosy.vercel.app/register/confirm/{uidb64}/{token}">
        http://frontend-two-rosy.vercel.app/register/confirm/{uidb64}/{token}</a>

        <p>If you didn't sign up for MinervaLMS or have received this email by mistake, please disregard it.
        Thank you for choosing MinervaLMS for your educational journey. </p>

        <The>Best regards,<br>
        The MinervaLMS Team</p>
        """,
    }


def forgot_email(email: str, token: str, uidb64: str) -> dict:
    return {
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


def contact_support_email(sender_email: str, sender_name: str, subject: str, email_body: str) -> dict:
    ticket_id = int(datetime.now().timestamp() * 1000)

    return {
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
