from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import login_view, register_view, send_email, modify_password_forgotten, lista_usuarios

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login_view, name='minerva_login_user'),
    path('lista/', lista_usuarios, name='minerva_user_list'),
    path('register/', register_view, name="minerva_register"),
    path('forget-password/', send_email, name="password_forgotten"),
    path('password-reset/<uidb64>/<token>',
         modify_password_forgotten, name="modify_password")
]
