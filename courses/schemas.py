import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

# Schemas used for API documentation

# Post material Schema
postMaterial_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.String(description="Module id")
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
        schema=coreschema.String(description="Material is extra")
    ),
    coreapi.Field(
        "order",
        required=True,
        location="form",
        type="integer",
        schema=coreschema.String(description="Material order")
    )
])

# Edit material Schema
editMaterial_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.String(description="Module id")
    ),
    coreapi.Field(
        "name",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Material name")
    ),
    coreapi.Field(
        "material_type",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Material type")
    ),
    coreapi.Field(
        "is_extra",
        required=False,
        location="form",
        type="boolean",
        schema=coreschema.String(description="Material is extra")
    ),
    coreapi.Field(
        "order",
        required=False,
        location="form",
        type="integer",
        schema=coreschema.String(description="Material order")
    )
])
