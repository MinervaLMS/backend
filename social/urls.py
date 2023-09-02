from django.urls import path

from .views import material_views

material_urls = [
    path(
        "material/like/<int:material_id>/<int:user_id>/",
        material_views.like_materail,
        name="like_material",
    ),
    path(
        "material/dislike/<int:material_id>/<int:user_id>/",
        material_views.like_materail,
        name="dislike_material",
    ),
]

urlpatterns = material_urls
