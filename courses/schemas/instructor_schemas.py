import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_instructor_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(description="User's id who will be instructor"),
        ),
        coreapi.Field(
            "course_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="Course's id in which the user will be instructor"
            ),
        ),
        coreapi.Field(
            "instructor_type",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(
                description="Type of instructor (E: Editor, T: Tutor, A: Assistant)"
            ),
        ),
    ]
)

get_instructor_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id who is instructor"),
        ),
        coreapi.Field(
            "course_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Course's id in which the user is instructor"
            ),
        ),
    ]
)

update_instructor_type_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id who is instructor"),
        ),
        coreapi.Field(
            "course_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Course's id in which the user is instructor"
            ),
        ),
        coreapi.Field(
            "instructor_type",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(
                description="New type of instructor (E: Editor, T: Tutor, A: Assistant)"
            ),
        ),
    ]
)

delete_instructor_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="User's id who is instructor to delete"
            ),
        ),
        coreapi.Field(
            "course_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Course's id in which the user is instructor to delete"
            ),
        ),
    ]
)
