from django.urls import path

from .views import comment_views

comment_urls = [
    path("comment/create/", comment_views.create_comment, name="create_comment"),
    path("comment/<int:comment_id>/", comment_views.get_comment, name="get_comment"),
    path(
        "comment/<int:comment_id>/replies/",
        comment_views.get_comment_replies,
        name="get_replies",
    ),
    path(
        "comment/update/<int:comment_id>/",
        comment_views.update_comment_fixed,
        name="delete_comment",
    ),
    path(
        "comment/delete/<int:comment_id>/",
        comment_views.delete_comment,
        name="delete_comment",
    ),
]

# TODO: These urls below should be in accounts app
user_urls = [
    path(
        "users/<int:user_id>/comments/<int:material_id>/",
        comment_views.get_user_comments,
        name="get_user_comments",
    ),
    path(
        "users/update/<int:user_id>/comment/<int:comment_id>/",
        comment_views.update_user_comment,
        name="update_user_comment",
    ),
    path(
        "users/delete/<int:user_id>/comment/<int:comment_id>/",
        comment_views.delete_user_comment,
        name="delete_user_comment",
    ),
]

material_urls = [
    path(
        "material/<int:material_id>/comments/",
        comment_views.get_material_comments,
        name="get_material_comments",
    ),
]

urlpatterns = comment_urls + user_urls + material_urls
