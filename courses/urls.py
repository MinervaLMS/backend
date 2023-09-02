from django.urls import path

from .views import (
    course_views,
    module_views,
    material_views,
    material_html_views,
    material_video_views,
    access_views,
)

course_urls = [
    path("course/create/", course_views.create_course, name="create_course"),
    path("course/<str:alias>/", course_views.get_course, name="get_course"),
    path(
        "course/update/<str:alias>/", course_views.update_course, name="update_course"
    ),
    path(
        "course/delete/<str:alias>/", course_views.delete_course, name="delete_course"
    ),
    path(
        "course/<str:alias>/modules/",
        course_views.get_modules_by_course,
        name="get_modules_by_course",
    ),
    path(
        "course/<str:alias>/<int:order>/",
        course_views.get_module_by_course_order,
        name="get_module_by_course_order",
    ),
    path(
        "course/<str:alias>/modules/update_order/",
        course_views.update_module_order,
        name="update_module_order",
    ),
]

module_urls = [
    path("module/create/", module_views.create_module, name="create_module"),
    path(
        "module/<int:module_id>/",
        module_views.get_module_by_id,
        name="get_module_by_id",
    ),
    path(
        "module/update/<int:module_id>/",
        module_views.update_module,
        name="update_module",
    ),
    path(
        "module/delete/<int:module_id>/",
        module_views.delete_module,
        name="delete_module",
    ),
    path(
        "module/<int:module_id>/materials/",
        module_views.get_materials_by_module,
        name="get_materials_by_module",
    ),
    path(
        "module/<int:module_id>/materials/<int:order>/",
        module_views.get_material_by_module_order,
        name="get_material_by_module_order",
    ),
    path(
        "module/<int:module_id>/materials/update_order/",
        module_views.update_material_order,
        name="update_material_order",
    ),
]

material_urls = [
    path("material/create/", material_views.create_material, name="create_material"),
    path(
        "material/<int:material_id>/", material_views.get_material, name="get_material"
    ),
    path(
        "material/update/<int:material_id>/",
        material_views.update_material,
        name="update_material",
    ),
    path(
        "material/delete/<int:material_id>/",
        material_views.delete_material,
        name="delete_material",
    ),
]

material_html_urls = [
    path(
        "material/html/create/",
        material_html_views.create_material_html,
        name="create_material_html",
    ),
    path(
        "material/html/<int:material_id>/",
        material_html_views.get_material_html,
        name="get_material_html",
    ),
    path(
        "material/html/update/<int:material_id>/",
        material_html_views.update_material_html,
        name="update_material_html",
    ),
    path(
        "material/html/delete/<int:material_id>/",
        material_html_views.delete_material_html,
        name="delete_material_html",
    ),
]

material_video_urls = [
    path(
        "material/video/create/",
        material_video_views.create_material_video,
        name="create_material_video",
    ),
    path(
        "material/video/<int:material_id>/",
        material_video_views.get_material_video,
        name="get_material_video",
    ),
    path(
        "material/video/update/<int:material_id>/",
        material_video_views.update_material_video,
        name="update_material_video",
    ),
    path(
        "material/video/delete/<int:material_video_id>/",
        material_video_views.delete_material,
        name="delete_material_video",
    ),
]

access_urls = [
    path("material/access/create/", access_views.create_access, name="create_access"),
    path(
        "material/access/<int:material_id>/<int:user_id>/",
        access_views.get_access,
        name="get_access",
    ),
    path("material/assess/", access_views.assess_material, name="assess_material"),
]

urlpatterns = (
    course_urls
    + module_urls
    + material_urls
    + material_html_urls
    + material_video_urls
    + access_urls
)
