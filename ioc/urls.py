from django.urls import path

from .views import (
    material_io_code_views,
    io_code_submission_views,
    io_code_submission_summary_views,
)


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

io_code_submission_urls = [
    path(
        "iocode/submission/create/",
        io_code_submission_views.create_io_code_submission,
        name="create_io_code_submission",
    ),
    path(
        "iocode/submission/<int:submission_id>/",
        io_code_submission_views.get_io_code_submission,
        name="get_io_code_submission",
    ),
    path(
        "iocode/submission/update/<int:submission_id>/",
        io_code_submission_views.update_io_code_submission,
        name="update_io_code_submission",
    ),
    path(
        "iocode/submission/delete/<int:submission_id>/",
        io_code_submission_views.delete_io_code_submission,
        name="delete_io_code_submission",
    ),
]

io_code_submission_summary_urls = [
    path(
        "iocode/submission/summary/<int:user_id>/<int:material_id>/",
        io_code_submission_summary_views.get_summary_by_user,
        name="get_summary_by_user",
    )
]
urlpatterns = material_io_code_urls + io_code_submission_urls + io_code_submission_summary_urls
