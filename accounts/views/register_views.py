from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, schema

from ..schemas import user_register_schema, confirm_email_schema, resend_confirmation_email_schema
from ..serializers import UserSerializer
from ..models import User
from ..helpers import *

@api_view(['POST'])
@schema(user_register_schema)
def user_register(request) -> JsonResponse:
    """
    View to user register in the database and send an email to confirm the account

    Args:
        request: request http with user data for register

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    token: str = confirmation_token_generator.make_token(user)
    uidb64: str = urlsafe_base64_encode(force_bytes(user.email))

    try:
        send_confirmation_email(user.email, user.first_name, token, uidb64)

        if not settings.DEBUG:
            return JsonResponse({"uidb64" : uidb64, "token": token}, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    except Exception:
        return JsonResponse({"message": "Email was not sent"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@schema(confirm_email_schema)
def confirm_email(request, uidb64: str, token: str) -> JsonResponse:
    """
    Confirm the user email after reading the token and uidb64 from the url

    Args:
        request: request http
        uidb64 (str): Base 64 encode of user email
        token (str): Temporary token to confirm email

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    email: str = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(email=email).first()

    if user is None or not confirmation_token_generator.check_token(user, token):
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save()

    return JsonResponse({"message": "Email was confirmed successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@schema(resend_confirmation_email_schema)
def resend_confirmation_email(request, uidb64: str) -> JsonResponse:
    """
    Resend the confirmation email after reading the uidb64 from the url

    Args:
        request: request http
        uidb64 (str): Base 64 encode of user email

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """


    email: str = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(email=email).first()
    token: str = confirmation_token_generator.make_token(user)

    try:
        send_confirmation_email(user.email, user.first_name, token, uidb64)

        return JsonResponse({"message": "Email was sent"}, status=status.HTTP_201_CREATED)
    except Exception:
        return JsonResponse({"message": "Email was not sent"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)