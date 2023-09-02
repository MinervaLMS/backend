import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_access_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="Material's id to which the access belongs"
            ),
        ),
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="User's id to which the access belongs"
            ),
        ),
    ]
)

get_access_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Material's id to which the access belongs"
            ),
        ),
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="User's id to which the access belongs"
            ),
        ),
    ]
)

update_access_like_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="Material's id to which the user wants to update the like"
            ),
        ),
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="User's id that wants to update the like"
            ),
        ),
    ]
)

update_access_dislike_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description=(
                    "Material's id to which the user wants to update the dislike"
                )
            ),
        ),
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="User's id that wants to update the dislike"
            ),
        ),
    ]
)

delete_access_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Material's id to which the access belongs"
            ),
        ),
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="User's id to which the access belongs"
            ),
        ),
    ]
)
