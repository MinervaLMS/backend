import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

get_summary_by_user_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.Integer(description="User's id to get his/her submission summary"),
        ),
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.Integer(description="Material's id to get its submission summary"),
        ),
    ]
)