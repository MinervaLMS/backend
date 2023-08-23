import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

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

get_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    )
])

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

delete_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    )
])

get_modules_by_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Course's alias")
    )
])

get_module_by_course_order_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Course's alias")
    ),
    coreapi.Field(
        "order",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Module's order")
    )
])

update_module_order_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Course's alias")
    )
])