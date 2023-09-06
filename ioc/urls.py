from django.urls import path

from .views import material_io_code_views

material_io_code_urls = [
    path(
        "material/iocode/create/",
        material_io_code_views.create_material_io_code,
        name="create_material_io_code",
    ),
    path(
        "material/iocode/<int:material_id>/",
        material_io_code_views.get_material_io_code,
        name="get_material_io_code",
    ),
    path(
        "material/iocode/update/<int:material_id>/",
        material_io_code_views.update_material_io_code,
        name="update_material_io_code",
    ),
    path(
        "material/iocode/delete/<int:material_io_code_id>/",
        material_io_code_views.delete_material,
        name="delete_material_io_code",
    ),
]

urlpatterns = (
    material_io_code_urls
)