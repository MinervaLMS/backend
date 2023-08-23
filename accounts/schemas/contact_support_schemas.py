import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

contact_support_email_schema = AutoSchema(manual_fields=[
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
        schema=coreschema.String(
            description="Text of the contact email written by the user")
    ),
])