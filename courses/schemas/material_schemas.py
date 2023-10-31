import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_material_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "module_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.Integer(
                description="Module's id from which you want to create the material",
            ),
        ),
        coreapi.Field(
            "name",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(description="Material name"),
        ),
        coreapi.Field(
            "material_type",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(description="Material type"),
        ),
        coreapi.Field(
            "content",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(
                description="The Markdown for the HTML material or "
                + "material. Only needed for the HTM type."
            ),
        ),
        coreapi.Field(
            "external_id",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(
                description="Link of the video related to a video material."
                + "Only needed for the VID type."
            ),
        ),
        coreapi.Field(
            "url",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(
                description="Link to the pdf file related to a pdf material."
                + "Only needed for the PDF type."
            ),
        ),
        coreapi.Field(
            "input",
            required=False,
            location="form",
            type="array",
            # TODO: Better description of this field
            schema=coreschema.Array(
                description="List of the inputs of cases."
                + "Only needed for the IOC type."
            ),
        ),
        coreapi.Field(
            "output",
            required=False,
            location="form",
            type="array",
            # TODO: Better description of this field
            schema=coreschema.Array(
                description="List of the outputs of cases."
                + "Only needed for the IOC type."
            ),
        ),
        coreapi.Field(
            "points",
            required=False,
            location="form",
            type="array",
            # TODO: Better description of this field
            schema=coreschema.Array(
                description="List of the points of cases."
                + "Only needed for the IOC type."
            ),
        ),
        coreapi.Field(
            "max_time",
            required=False,
            location="form",
            type="integer",
            # TODO: Better description of this field
            schema=coreschema.Integer(
                description="The maximum time an ioc is allowed to run."
                + "Only needed for the IOC type."
            ),
        ),
        coreapi.Field(
            "max_memory",
            required=False,
            location="form",
            type="integer",
            # TODO: Better description of this field
            schema=coreschema.Integer(
                description="The maximum memory an ioc will be allowed."
                + " Should be grater or equal than 300."
                + " Only needed for the IOC type."
            ),
        ),
        coreapi.Field(
            "is_extra",
            required=True,
            location="form",
            type="boolean",
            schema=coreschema.Boolean(description="Material is extra or not"),
        ),
    ]
)

get_material_schema = AutoSchema(
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

update_material_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Material's id to update it"),
        ),
        coreapi.Field(
            "name",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(description="New material name"),
        ),
        coreapi.Field(
            "material_type",
            required=False,
            location="form",
            type="string",
            schema=coreschema.String(description="New material type"),
        ),
        coreapi.Field(
            "is_extra",
            required=False,
            location="form",
            type="boolean",
            schema=coreschema.String(description="Material is extra or not"),
        ),
    ]
)

delete_material_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Material id"),
        ),
    ]
)
