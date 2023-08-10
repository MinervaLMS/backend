from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from django.http import JsonResponse

from .models import User
from .serializers import MinervaUserSerializer, MinervaUserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from . import schemas
from .helpers import send_forgot_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
# Create your views here.


@api_view(['POST'])
@schema(schemas.login_schema)
def login_view(request) -> JsonResponse:
    """
    View to user login

    Args:
        request: http request with user data for login

    Returns:
        response: http response {json format}
    """

    serializer = MinervaUserLoginSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):

        user = serializer.validated_data
        serializer = MinervaUserSerializer(user)
        tokens: dict[str, str] = get_tokens_for_user(user)
        data = serializer.data
        data["tokens"] = tokens

        return JsonResponse(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@schema(schemas.register_schema)
def register_view(request) -> JsonResponse:
    """
    View to user register

    Args:
        request: request http with user data register

    Returns:
        response: http response (json format)
    """
    serializer = MinervaUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user: User | None) -> dict[str, str]:
    """
    Create refresh and access token with email

    Args:
        user: Minerva Database user

    Returns:
        tokens: Refresh token and access token.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Used to test view for login functionality
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_usuarios(request) -> JsonResponse:
    """
    Get all users in the Minerva database, but only the MinervaUserSerializer fields
    ("email", "first_name", "last_name").

    Returns:
        Json response with the fields of the serialized users if the user making the request is Authenticated,
        else throws 401 Unauthorized status
    """

    usuarios = User.objects.all()
    serializer = MinervaUserSerializer(usuarios, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@schema(schemas.pass_forgot_schema)
def send_email(request) -> JsonResponse:
    '''
    Send an email to the user after he introduces his email, if the email is not in DB then it returns an error message

    Returns:
        Json response saying that the email was sent if the email was found, else throws a 404 error (Not found)
    '''

    if not "email" in request.data:
        return JsonResponse({"message": "Email was not sent"}, status=status.HTTP_400_BAD_REQUEST)

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
    '''
    After getting into the link the request read the token to get the user, then it changes the password

    Returns:
        Json response saying that the password was changed, else throws a 404 error if the user was not found or 400 error
    '''
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
