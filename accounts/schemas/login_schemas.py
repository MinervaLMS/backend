import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

user_login_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "email",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User email")
    ),
    coreapi.Field(
        "password",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User password")
    )
])