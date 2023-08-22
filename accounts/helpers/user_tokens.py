from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User

def get_tokens_for_user(user: User | None) -> dict[str, str]:
    """
    Create refresh and access token with email

    Args:
        user (User): Minerva Database user

    Returns:
        tokens (dict): Refresh token and access token.
    """

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }