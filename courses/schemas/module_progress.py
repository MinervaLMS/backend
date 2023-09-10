import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_module_progress_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="User id"
            ),
        ),
        coreapi.Field(
            "module_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(description="Module id"),
        ),
    ]
)

get_module_progress_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to get it"),
        ),
        coreapi.Field(
            "module_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Module's id to get it"),
        ),
    ]
)

update_module_progress_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to get it"),
        ),
        coreapi.Field(
            "module_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Module's id to get it"),
        ),
        coreapi.Field(
            "material_type",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(
                description="Material's type to update it"),
        ),
        coreapi.Field(
            "type",
            required=True,
            location="form",
            type="boolean",
            schema=coreschema.String(description="Type of update"),
        ),

    ]
)

reload_module_progress_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to get it"),
        ),
        coreapi.Field(
            "module_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Module's id to get it"),
        ),
    ]
)
