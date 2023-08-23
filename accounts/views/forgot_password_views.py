from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, schema

from ..schemas import forgot_my_password_schema, modify_forgotten_password_schema
from ..models import User
from ..helpers import *

@api_view(['POST'])
@schema(forgot_my_password_schema)
def forgot_my_password(request) -> JsonResponse:
    """
    Send an email to an user to reset password

    Args:
        request: request http with user email

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    email_validator = EmailValidator()

    if not "email" in request.data:
        return JsonResponse({"email": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

    email: str = request.data["email"]

    try:
        email_validator(email)
    except ValidationError:
        return JsonResponse({"message": "Enter a valid email address."}, status=status.HTTP_400_BAD_REQUEST)

    user_using = User.objects.filter(email=email).first()

    if not user_using:
        return JsonResponse({"message": "No user with this email."}, status=status.HTTP_404_NOT_FOUND)

    token: str = default_token_generator.make_token(user_using)
    uidb64: str = urlsafe_base64_encode(force_bytes(user_using.pk))

    try:
        send_forgot_email(email, token, uidb64)
    except Exception:
        return JsonResponse({"message": "Email was not sent"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({"message": "Email was sent"}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@schema(modify_forgotten_password_schema)
def modify_forgotten_password(request, uidb64: str, token: str) -> JsonResponse:
    """
    Changes the user password after reading the token and uidb64 from the url

    Args:
        request: request http
        uidb64 (str): Base 64 encode of user id
        token (str): Temporary token to reset password

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    uid: str = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=uid).first()

    if user is None or not default_token_generator.check_token(user, token):
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    data = JSONParser().parse(request)
    new_password: str = data["password"]

    if new_password == '':
        return JsonResponse({"message": "Password is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(new_password)
    user.save()

    return JsonResponse({"message": "Password was changed successfully"}, status=status.HTTP_200_OK)