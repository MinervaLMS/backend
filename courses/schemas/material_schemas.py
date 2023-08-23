import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_material_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.String(
            description="Module's id from which you want to create the material")
    ),
    coreapi.Field(
        "name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Material name")
    ),
    coreapi.Field(
        "material_type",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Material type")
    ),
    coreapi.Field(
        "is_extra",
        required=True,
        location="form",
        type="boolean",
        schema=coreschema.String(description="Material is extra or not")
    ),
    coreapi.Field(
        "order",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.String(description="Material order")
    )
])

get_material_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "material_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Material's id to get it")
    ),
])

update_material_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "material_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Material's id to update it")
    ),
    coreapi.Field(
        "name",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="New material name")
    ),
    coreapi.Field(
        "material_type",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="New material type")
    ),
    coreapi.Field(
        "is_extra",
        required=False,
        location="form",
        type="boolean",
        schema=coreschema.String(description="Material is extra or not")
    ),
])

delete_material_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "material_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Material id")
    ),
])