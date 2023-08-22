import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

user_register_schema = AutoSchema(manual_fields=[
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
    ),
    coreapi.Field(
        "first_name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User first name")
    ),
    coreapi.Field(
        "last_name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User last name")
    )
])

confirm_email_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "uidb64",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="User email encoded")
    ),
    coreapi.Field(
        "token",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="User token link")
    ),
])

resend_confirmation_email_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "uidb64",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="User email encoded")
    ),
])