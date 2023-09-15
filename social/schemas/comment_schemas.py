import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

create_comment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="Material's id which has been commented"
            ),
        ),
        coreapi.Field(
            "user_id",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(
                description="User's id who commented the material"
            ),
        ),
        coreapi.Field(
            "parent_comment_id",
            required=False,
            location="form",
            type="integer",
            schema=coreschema.String(description="Comment's id which is being replied"),
        ),
        coreapi.Field(
            "content",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(description="Comment's content"),
        ),
        coreapi.Field(
            "fixed",
            required=False,
            location="form",
            type="integer",
            schema=coreschema.String(description="Fixed's order of comment"),
        ),
    ]
)

get_comment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "comment_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Comment's id to get"),
        ),
    ]
)

get_comment_replies_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "comment_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Comment's id to get its replies"),
        ),
    ]
)

update_comment_fixed_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "comment_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Comment's id to update its fixed value"
            ),
        ),
        coreapi.Field(
            "fixed",
            required=True,
            location="form",
            type="integer",
            schema=coreschema.String(description="New fixed value"),
        ),
    ]
)

delete_comment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "comment_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Comment's id to delete"),
        ),
    ]
)

# TODO: These schemas below should be in accounts app (for user)
get_user_comments_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to get his/her comments"),
        ),
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(
                description="Material's id to get its comments done by the user"
            ),
        ),
    ]
)

update_user_comment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to update his/her comment"),
        ),
        coreapi.Field(
            "comment_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Comment's id to update"),
        ),
        coreapi.Field(
            "content",
            required=True,
            location="form",
            type="string",
            schema=coreschema.String(description="New content of the comment"),
        ),
    ]
)

delete_user_comment_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "user_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="User's id to delete his/her comment"),
        ),
        coreapi.Field(
            "comment_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String(description="Comment's id to delete"),
        ),
    ]
)

# TODO: These schemas below should be in courses app (for material)
get_material_comments_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            "material_id",
            required=True,
            location="path",
            type="integer",
            schema=coreschema.String("Material's id to get its comments"),
        ),
    ]
)
