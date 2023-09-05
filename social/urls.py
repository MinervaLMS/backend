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
        "comment/delete/<int:comment_id>/",
        comment_views.delete_comment,
        name="delete_comment",
    ),
]

# TODO: These urls below should be in accounts app
user_ursl = [
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

urlpatterns = comment_urls + user_ursl
