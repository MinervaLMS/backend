from django.urls import path

from .views import institution_views

institution_urls = [
    path(
        "institution/create/",
        institution_views.create_institution,
        name="create_institution",
    ),
    path(
        "institution/<int:institution_id>/",
        institution_views.get_institution,
        name="get_institution",
    ),
    path(
        "institution/update/<int:institution_id>/",
        institution_views.update_institution,
        name="update_institution",
    ),
    path(
        "institution/delete/<int:institution_id>/",
        institution_views.delete_institution,
        name="delete_institution",
    ),
]

urlpatterns = institution_urls
