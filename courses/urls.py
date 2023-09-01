from django.urls import path

from .views import *

course_urls = [
    path('course/create/', create_course, name='create_course'),
    path('course/<str:alias>/', get_course, name='get_course'),
    path('course/update/<str:alias>/', update_course, name='update_course'),
    path('course/delete/<str:alias>/', delete_course, name='delete_course'),
    path('course/<str:alias>/modules/',
         get_modules_by_course, name="get_modules_by_course"),
    path('course/<str:alias>/<int:order>/', get_module_by_course_order,
         name="get_module_by_course_order"),
    path('course/<str:alias>/modules/update_order/',
         update_module_order, name='update_module_order')
]

module_urls = [
    path('module/create/', create_module, name='create_module'),
    path('module/<int:module_id>/', get_module_by_id, name='get_module_by_id'),
    path('module/update/<int:module_id>/', update_module, name='update_module'),
    path('module/delete/<int:module_id>/', delete_module, name='delete_module'),
    path('module/<int:module_id>/materials/',
         get_materials_by_module, name="get_materials_by_module"),
    path('module/<int:module_id>/materials/<int:order>/',
         get_material_by_module_order, name="get_material_by_module_order"),
    path('module/<int:module_id>/materials/update_order/',
         update_material_order, name='update_material_order'),
]

material_urls = [
    path('material/create/', create_material, name="create_material"),
    path('material/<int:material_id>/', get_material, name="get_material"),
    path('material/update/<int:material_id>/',
         update_material, name='update_material'),
    path('material/delete/<int:material_id>/',
         delete_material, name='delete_material'),
]

material_video_urls = [
     path('material/video/create/', create_material_video, name="create_material_video"),
     path('material/video/<int:material_id>/', get_material_video, name="get_material_video"),
     path('material/video/update/<int:material_id>/',
         update_material_video, name='update_material_video'),
     path('material/video/delete/<int:material_video_id>/',
         delete_material, name='delete_material_video'),
]
urlpatterns = course_urls + module_urls + material_urls + material_video_urls
