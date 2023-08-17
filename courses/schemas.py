import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

# Schemas used for API documentation

#Create Course Schema

create_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "name",
        required=True,
        location="form",
        schema=coreschema.String(description="Course name")
    ),
    coreapi.Field(
        "alias",
        required=True,
        location="form",
        schema=coreschema.String(description="Course alias")
    ),
    coreapi.Field(
        "description",
        required=False,
        location="form",
        schema=coreschema.String(description="Course description")
    )
])

#Read Course Schema
get_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    )
])

#Update Course Schema
update_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "name",
        required=False,
        location="form",
        schema=coreschema.String(description="Course name")
    ),
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    ),
    coreapi.Field(
        "description",
        required=False,
        location="form",
        schema=coreschema.String(description="Course description")
    )
])

#Delete Course Schema
delete_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    )
])