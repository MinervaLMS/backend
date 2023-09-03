from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, schema

from ..schemas import contact_support_schemas as schemas
from ..helpers import emails


@api_view(["POST"])
@schema(schemas.contact_support_email_schema)
def contact_support_email(request) -> JsonResponse:
    """
    Send an email to our support email with the user email and message

    Args:
        request: request http with user email

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    email_validator = EmailValidator()

    required_fields = ["sender_email", "sender_name", "subject", "email_body"]
    error_messages: dict = {}

    for field in required_fields:
        if field not in request.data:
            error_messages[field] = ["This field is required."]
        elif field == "sender_email":
            try:
                email_validator(request.data[field])
            except ValidationError:
                error_messages[field] = ["Enter a valid email address."]

    if error_messages:
        return JsonResponse(error_messages, status=status.HTTP_400_BAD_REQUEST)

    sender_email: str = request.data["sender_email"]
    sender_name: str = request.data["sender_name"]
    subject: str = request.data["subject"]
    email_body: str = request.data["email_body"]

    try:
        emails.send_contact_support_email(
            sender_email, sender_name, subject, email_body
        )
    except Exception:
        return JsonResponse(
            {"message": "Email was not sent"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JsonResponse({"message": "Email was sent"}, status=status.HTTP_200_OK)
