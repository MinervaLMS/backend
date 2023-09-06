import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

get_user_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="string",
            schema=coreschema.String(description="User id"),
        ),
    ]
)

get_user_courses_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="string",
            schema=coreschema.String(description="User id"),
        ),
    ]
)
