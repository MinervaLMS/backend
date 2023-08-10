import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

# Schemas used for API documentation
# Login Schema
login_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string",
                  schema=coreschema.String(description="User email")),
    coreapi.Field("password", required=True, location="form", type="string",
                  schema=coreschema.String(description="User password"))
])
# Register Schema
register_schema = AutoSchema(manual_fields=[
    coreapi.Field("first_name", required=True, location="form", type="string",
                  schema=coreschema.String(description="User first name")),
    coreapi.Field("last_name", required=True, location="form", type="string",
                  schema=coreschema.String(description="User last name")),
    coreapi.Field("email", required=True, location="form", type="string",
                  schema=coreschema.String(description="User email")),
    coreapi.Field("password", required=True, location="form", type="string",
                  schema=coreschema.String(description="User password"))
])
# Email send forgot pass Schema
pass_forgot_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string",
                  schema=coreschema.String(description="User email"))
])
# Reset pass Schema
pass_forgot_modify = AutoSchema(manual_fields=[
    coreapi.Field("uidb64", required=True, location="path", type="string",
                  schema=coreschema.String(description="User id encoded")),
    coreapi.Field("token", required=True, location="path", type="string",
                  schema=coreschema.String(description="User token link")),
    coreapi.Field("password", required=True, location="form", type="string",
                  schema=coreschema.String(description="User password"))
])
