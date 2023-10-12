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

get_user_materials_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="User's id who has accessed to the materials"
            ),
        ),
        coreapi.Field(
            "module_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Module's id which materials belongs to"
            ),
        ),
    ]
)
