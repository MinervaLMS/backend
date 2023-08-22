import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

# Schemas used for API documentation

# Create Course Schema
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

# Read Course Schema
get_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    )
])

# Update Course Schema
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

# Delete Course Schema
delete_course_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        schema=coreschema.String(description="Course alias")
    )
])

# Create material
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

# Get materials by module
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

# get_material by id
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

# Update material order
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

# Delete material
delete_material_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "material_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Material id")
    ),
])

# Module
# Create module
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
# Get module
get_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Module's id")
    )])
# Delete module
delete_module_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "module_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.String(description="Module's id")
    )])
# Update module order
update_module_order_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "alias",
        required=True,
        location="path",
        type="string",
        schema=coreschema.String(description="Course's alias")
    )
])
# Update module
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
# List modules by course
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
