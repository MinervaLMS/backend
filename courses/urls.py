from django.urls import path
from . import views

urlpatterns = [
    path('course/create/', views.create_course, name='create_course'),
    path('course/get/<str:alias>/', views.get_course, name='get_course'),
    path('course/update/<str:alias>/', views.update_course, name='update_course'),
    path('course/delete/<str:alias>/', views.delete_course, name='delete_course'),
    
    path('material/create/', views.create_material, name="create_material"),
    path('module/<int:module_id>/materials/', views.get_materials_by_module, name="get_materials_by_module"),
    path('material/<int:material_id>/', views.get_material, name="get_material"),
    path('material/update/<int:material_id>/', views.update_material, name='update_material'),
    path('module/<int:module_id>/materials/update_order', views.update_material_order, name='update_material_order'),
    path('material/delete/<int:material_id>/', views.delete_material, name='delete_material'),
]