from django.urls import path
from . import views

course_urls = [
    path('course/create/', views.create_course, name='create_course'),
    path('course/<str:alias>/', views.get_course, name='get_course'),
    path('course/update/<str:alias>/', views.update_course, name='update_course'),
    path('course/delete/<str:alias>/', views.delete_course, name='delete_course'),
]

module_urls = [
    path('module/<int:module_id>/materials/', views.get_materials_by_module, name="get_materials_by_module"),
    path('module/<int:module_id>/materials/update_order/', views.update_material_order, name='update_material_order'),
]

material_urls = [
    path('material/create/', views.create_material, name="create_material"),
    path('material/<int:material_id>/', views.get_material, name="get_material"),
    path('material/update/<int:material_id>/', views.update_material, name='update_material'),
    path('material/delete/<int:material_id>/', views.delete_material, name='delete_material'),
]


urlpatterns = course_urls + module_urls + material_urls

