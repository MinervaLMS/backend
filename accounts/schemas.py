import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

# Schemas used for API documentation
login_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string",
                  schema=coreschema.String(description="User email")),
    coreapi.Field("password", required=True, location="form", type="string",
                  schema=coreschema.String(description="User password"))
])

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

pass_forgot_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string",
                  schema=coreschema.String(description="User email"))
])

pass_forgot_modify = AutoSchema(manual_fields=[
    coreapi.Field("token", required=True, location="path", type="string",
                  schema=coreschema.String(description="User token link")),
    coreapi.Field("password", required=True, location="form", type="string",
                  schema=coreschema.String(description="User password"))
])
