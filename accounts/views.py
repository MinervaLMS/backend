from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from django.http import JsonResponse

from .models import User
from .serializers import MinervaUserSerializer
from ast import literal_eval
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

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
    user_data: dict = literal_eval(request.body.decode('utf-8'))

    # TODO: cuando el email sea unique, filtrar por email
    user : User | None = User.objects.filter(username=user_data['username']).first()
    if user:
        token: dict[str, str] = get_tokens_for_user(user)
        return JsonResponse(token)

    # TODO: definir un estandar de respuesta para todas las responses de la API
    response = Response("No se encontró el usuario", status=404)
    return response

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