from django.contrib import admin

from ..models.comment import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "material_id",
        "user_id",
        "parent_comment_id",
        "post_date",
        "content",
        "fixed",
    )


# Register your models here.
admin.site.register(Comment, CommentAdmin)
