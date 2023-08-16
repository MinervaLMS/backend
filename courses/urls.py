from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('create-Material/', views.postMaterial_view, name="create_material"),
    path('view-Material/', views.material_list, name="view_material"),
    path('update-material/<int:material_id>/', views.materialChange, name='update_material'),
    path('delete_material/<int:material_id>', views.delete_material_view, name='delete_material'),
]