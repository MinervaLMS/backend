import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

# Schemas used for API documentation

# Login Schema
login_schema = AutoSchema(manual_fields=[
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

# Register Schema
register_schema = AutoSchema(manual_fields=[
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

# Email send forgot password Schema
pass_forgot_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "email",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="User email")
    ),
])

# Reset password Schema
pass_forgot_modify_schema = AutoSchema(manual_fields=[
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

# Email send contact Schema
contact_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "sender_email",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Sender email")
    ),
    coreapi.Field(
        "sender_name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Sender name")
    ),
    coreapi.Field(
        "subject",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Subject of the email")
    ),
    coreapi.Field(
        "email_body",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Text of the contact email written by the user")
    ),
])

confirmation_email_schema = AutoSchema(manual_fields=[
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