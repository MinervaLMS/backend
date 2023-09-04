import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_institution_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "name",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution name")
    ),
    coreapi.Field(
        "alias",
        required=True,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution alias")
    ),
    coreapi.Field(
        "description",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution description")
    ),
    coreapi.Field(
        "url",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution URL")
    )
])

get_institution_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "institution_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.Integer(description="Institution ID")
    )
])

update_institution_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "institution_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.Integer(description="Institution ID")
    ),
    coreapi.Field(
        "name",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution name")
    ),
    coreapi.Field(
        "alias",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution alias")
    ),
    coreapi.Field(
        "description",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution description")
    ),
    coreapi.Field(
        "url",
        required=False,
        location="form",
        type="string",
        schema=coreschema.String(description="Institution URL")
    )
])

delete_institution_schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "institution_id",
        required=True,
        location="path",
        type="integer",
        schema=coreschema.Integer(description="Institution ID")
    )
])