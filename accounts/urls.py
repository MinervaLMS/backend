from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

# TODO: Change contact/ endpoint to an independent app in the future

register_urls = [
     path('register/', views.user_register, name="user_register"),
     path('register/confirm/<str:uidb64>/<str:token>', views.confirm_email, name="user_confirm_email"),
     path('register/resend/<str:uidb64>/', views.resend_confirmation_email, name="user_resend_confirmation_email"),
]

login_urls = [
     path('login/', views.user_login, name='user_login'),
     path('login/token/refresh/', TokenRefreshView.as_view(), name='user_token_refresh'),
]

password_reset_urls = [
     path('forgot-my-password/', views.forgot_my_password, name="user_forgot_my_password"),
     path('forgot-my-password/<str:uidb64>/<str:token>', views.modify_forgotten_password, name="user_modify_password"),
]

extra_urls = [
     path('users/', views.get_all_users, name='user_list'),
     path('contact/', views.contact_support_email, name="support_contact"),
]

urlpatterns = register_urls + login_urls + password_reset_urls + extra_urls