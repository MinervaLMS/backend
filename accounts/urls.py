from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import login_view, register_view

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('login/', login_view, name='minerva_login_user'),
    # path('lista/', lista_usuarios, name='minerva_user_list'),
    path('register/', register_view, name="minerva_register"),
]