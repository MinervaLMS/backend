from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.register_view, name="user_register"),
    path('login/', views.login_view, name='user_login'),
    path('list/', views.user_list, name='user_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-my-password/', views.forgot_my_password, name="forgot_my_password"),
    path('password-reset/<uidb64>/<token>', views.modify_password_forgotten, name="modify_password"),
    path('contact/', views.contact_email, name="contact"),
]
