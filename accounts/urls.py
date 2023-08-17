from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

# TODO: Change contact/ endpoint to an independent app in the future

urlpatterns = [
    path('register/', views.user_register, name="user_register"),
    path('register/confirm/<uidb64>/<token>',
         views.confirm_email, name="user_confirm_email"),

    path('login/', views.user_login, name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='user_token_refresh'),

    path('forgot-my-password/', views.forgot_my_password,
         name="user_forgot_my_password"),
    path('password-reset/<uidb64>/<token>',
         views.modify_forgotten_password, name="user_modify_password"),

    path('users/', views.get_all_users, name='user_list'),

    path('contact/', views.contact_support_email, name="support_contact"),
]
