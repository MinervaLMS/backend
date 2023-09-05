from django.urls import path

from .views import comment_views

comment_urls = [
    path("comment/create/", comment_views.create_comment, name="create_comment"),
    path("comment/<int:comment_id>/", comment_views.get_comment, name="get_comment"),
    path(
        "comment/replies/<int:comment_id>/",
        comment_views.get_comment_replies,
        name="get_replies",
    ),
    path(
        "comment/replies/<int:comment_id>/",
        comment_views.get_comment_replies,
        name="get_replies",
    ),
    path(
        "comment/delete/<int:comment_id>/",
        comment_views.delete_comment,
        name="delete_comment",
    ),
]

# TODO: These urls below should be in accounts app
user_ursl = [
    path(
        "user/comments/<int:user_id>/<int:material_id>/",
        comment_views.get_user_comments,
        name="get_user_comments",
    ),
    path(
        "user/comment/update/<int:user_id>/<int:comment_id>/",
        comment_views.update_user_comment,
        name="update_user_comment",
    ),
    path(
        "user/comment/delete/<int:user_id>/<int:comment_id>/",
        comment_views.delete_user_comment,
        name="delete_user_comment",
    ),
]

urlpatterns = comment_urls + user_ursl
