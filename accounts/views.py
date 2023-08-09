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
    data = JSONParser().parse(request)
    serializer = MinervaUserSerializer(data=data)
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