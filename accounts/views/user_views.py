from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from ..models.user import User
from ..serializers.user_serializer import UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request) -> JsonResponse:
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
