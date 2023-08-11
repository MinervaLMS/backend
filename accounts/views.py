from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status

from .serializers import UserSerializer, UserLoginSerializer
from .helpers import send_forgot_email, get_tokens_for_user
from .models import User
from . import schemas

@api_view(['POST'])
@schema(schemas.login_schema)
def login_view(request) -> JsonResponse:
    """
    View to user login using email and password

    Args:
        request: http request with user data for login

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data
        serializer = UserSerializer(user)
        tokens: dict[str, str] = get_tokens_for_user(user)
        data = serializer.data
        data["tokens"] = tokens

        return JsonResponse(data=data, status=status.HTTP_200_OK)

@api_view(['POST'])
@schema(schemas.register_schema)
def register_view(request) -> JsonResponse:
    """
    View to user register in the database

    Args:
        request: request http with user data for register

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@schema(schemas.pass_forgot_schema)
def forgot_my_password(request) -> JsonResponse:
    """
    Send an email to an user to reset password

    Args:
        request: request http with user email

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    if not "email" in request.data:
        return JsonResponse({"message": "Email was sent"}, status=status.HTTP_400_BAD_REQUEST)

    email: str = request.data["email"]
    user_using = User.objects.filter(email=email).first()

    if not user_using:
        return JsonResponse({"message": "No user with this email"}, status=status.HTTP_404_NOT_FOUND)

    token: str = default_token_generator.make_token(user_using)
    uidb64: str = urlsafe_base64_encode(force_bytes(user_using.pk))
    send_forgot_email(email, token, uidb64)

    return JsonResponse({"message": "Email was sent"}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@schema(schemas.pass_forgot_modify)
def modify_password_forgotten(request, uidb64: str, token: str) -> JsonResponse:
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
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    data = JSONParser().parse(request)
    new_password: str = data["password"]

    if new_password == '':
        return JsonResponse({"message": "Password is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(new_password)
    user.save()

    return JsonResponse({"message": "Password was changed successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request) -> JsonResponse:
    """
    Get all users in the database, but only returns the UserSerializer
    fields ("email", "first_name", "last_name").

    Args:
        request: request http with user email

    Returns:
        Json response with the fields of the serialized users if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return JsonResponse(serializer.data, safe=False)