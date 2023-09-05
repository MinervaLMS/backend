import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

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
