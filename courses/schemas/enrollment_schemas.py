import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_enrollment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(description="User's id to be enrolled"),
        ),
        coreapi.Field(
            "course_alias",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(
                description="Course's alias in which the user will be enrolled"
            ),
        ),
    ]
)

get_enrollment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to get his enrollment"),
        ),
        coreapi.Field(
            "course_alias",
            required=True,
            location="path",
            type="string",
            schema=coreschema.String(
                description="Course's alias in which user is enrolled"
            ),
        ),
    ]
)

appraise_course_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "alias",
            required=True,
            location="path",
            type="string",
            schema=coreschema.String(description="Course alias"),
        ),
        coreapi.Field(
            "stars",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(description="Appraisal stars from 1 to 10"),
        ),
        coreapi.Field(
            "comment",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(description="Appraisal comment"),
        ),
    ]
)
