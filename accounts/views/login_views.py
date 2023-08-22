from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, schema

from ..schemas import user_login_schema
from ..serializers import *
from ..helpers import *


@api_view(['POST'])
@schema(user_login_schema)
def user_login(request) -> JsonResponse:
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