import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "course_id",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.String(description="Course's id")
    ),
    coreapi.Field(
        "name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Module's name")
    ),
    coreapi.Field(
        "order",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.String(description="Module's name")
    )]
)

get_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Module's id")
    )])

update_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Module's id")
    ),
    coreapi.Field(
        "name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Module's name")
    )
])

delete_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Module's id")
    )
])

get_materials_by_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(
            description="Module's id from which you want to get the materials")
    ),
])

get_material_by_module_order_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Module ID")
    ),
    coreapi.Field(
        "order",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Material's order")
    )
])

update_material_order_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(
            description="Module's id from which you want to update material order")
    ),
])