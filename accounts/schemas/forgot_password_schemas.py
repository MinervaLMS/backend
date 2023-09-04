import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

forgot_my_password_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "email",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User email")
    ),
])

# Reset password Schema
modify_forgotten_password_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "uidb64",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="User id encoded")
    ),
    coreapi.Field(
        "token",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="User token link")
    ),
    coreapi.Field(
        "password",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User password")
    )
])
