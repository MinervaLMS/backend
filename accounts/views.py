from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .serializers import MinervaUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# Create your views here.

@api_view(['POST'])
def login_view(request) -> JsonResponse:
    """
    View to user login

    Args:
        request: request http with user data login

    Returns:
        response: http response (json format)
    """
    user_data: dict = request.data
    password: str = user_data['password']

    # TODO: cuando el email sea unique, filtrar por email
    user : User | None = User.objects.filter(username=user_data['username']).first()

    if not user:
        raise AuthenticationFailed("User not found, check credentials.")

    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect password.")


    # TODO: definir un estandar de respuesta para todas las responses de la API
    token: dict[str, str] = get_tokens_for_user(user)
    return JsonResponse(token)

@api_view(['POST'])
def register_view(request) -> JsonResponse:
    """
    View to user register

    Args:
        request: request http with user data login

    Returns:
        response: http response (json format)
    """
    data = JSONParser().parse(request)
    serializer = MinervaUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

def get_tokens_for_user(user: User | None) -> dict[str, str]:
    """
    Create refresh and access token with email

    Args:
        user: Minerva Database user

    Returns:
        tokens: Refresh token and access token.
    """
    refresh = RefreshToken.for_user(user)
    refresh["email"] = user.email

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# @api_view(['GET'])
# def lista_usuarios(request):
#     usuarios = User.objects.all()
#     serializer = MinervaUserSerializer(usuarios, many=True)
#     return Response(serializer.data)