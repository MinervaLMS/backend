import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_material_html_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="""
                Material's id from which you want
                to create the HTML content
                """
            ),
        ),
        coreapi.Field(
            "content",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(
                description="""
                HTML (Markdown) content of the material.
                It should be a string with newlines and tabs. Max
                Markdown storage is about 100000 characters
                """
            ),
        ),
    ]
)

get_material_html_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Material's id to get its HTML content"
            ),
        ),
    ]
)

update_material_html_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Material's id to update its HTML content"
            ),
        ),
        coreapi.Field(
            "content",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(description="New HTML (Markdown) content"),
        ),
    ]
)

delete_material_html_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Material's id to delete its HTML content"
            ),
        ),
    ]
)
