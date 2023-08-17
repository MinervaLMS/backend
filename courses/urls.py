from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('material/create/', views.create_material, name="create_material"),
    path('module/<int:module_id>/materials/', views.get_materials_by_module, name="get_materials_by_module"),
    path('material/<int:material_id>/', views.get_material, name="get_material"),
    path('material/update/<int:material_id>/', views.update_material, name='update_material'),
    path('module/<int:module_id>/materials/update_order', views.update_material_order, name='update_material_order'),
    path('material/delete/<int:material_id>/', views.delete_material, name='delete_material'),
]