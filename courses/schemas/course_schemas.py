import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Course name")
    ),
    coreapi.Field(
        "alias",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Course alias")
    ),
    coreapi.Field(
        "description",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Course description")
    ),
    coreapi.Field(
        "institution_id",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="ID of the institution")
    ),
    coreapi.Field(
        "parent_course_id",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="ID of the parent course")
    ),
    coreapi.Field(
        "course_instructional_materials",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Instructional materials for the course")
    ),
    coreapi.Field(
        "course_assessment_materials",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Assessment materials for the course")
    ),
    coreapi.Field(
        "course_extra_materials",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Extra materials for the course")
    ),
    coreapi.Field(
        "min_assessment_progress",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Minimum assessment progress")
    ),
    coreapi.Field(
        "average_stars",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Average stars for the course")
    ),
    coreapi.Field(
        "appraisals",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Number of appraisals for the course")
    ),
    coreapi.Field(
        "comments",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Number of comments for the course")
    )
])

get_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Course alias")
    )
])

update_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "name",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Course name")
    ),
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Course alias")
    ),
    coreapi.Field(
        "description",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Course description")
    ),
    coreapi.Field(
        "institution_id",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="ID of the institution")
    ),
    coreapi.Field(
        "parent_course_id",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="ID of the parent course")
    ),
    coreapi.Field(
        "course_instructional_materials",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Instructional materials for the course")
    ),
    coreapi.Field(
        "course_assessment_materials",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Assessment materials for the course")
    ),
    coreapi.Field(
        "course_extra_materials",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Extra materials for the course")
    ),
    coreapi.Field(
        "min_assessment_progress",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Minimum assessment progress")
    ),
    coreapi.Field(
        "average_stars",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Average stars for the course")
    ),
    coreapi.Field(
        "appraisals",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Number of appraisals for the course")
    ),
    coreapi.Field(
        "comments",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.Integer(description="Number of comments for the course")
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