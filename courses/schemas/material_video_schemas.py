import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_material_video_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "external_id",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(
                description="Video's id from which you want to create the material"
            ),
        ),
        coreapi.Field(
            "material_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(description="Material id"),
        ),
    ]
)

get_material_video_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Material's id to get it"),
        ),
    ]
)

update_material_video_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Material's id to update it"),
        ),
        coreapi.Field(
            "external_id",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(description="New youtube link for this material"),
        ),
    ]
)

delete_material_video_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_video_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Material id"),
        ),
    ]
)
