from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

# TODO: Change contact/ endpoint to an independent app in the future

register_urls = [
     path('register/', user_register, name="user_register"),
     path('register/confirm/<str:uidb64>/<str:token>', confirm_email, name="user_confirm_email"),
     path('register/resend/<str:uidb64>/', resend_confirmation_email, name="user_resend_confirmation_email"),
]

login_urls = [
     path('login/', user_login, name='user_login'),
     path('login/token/refresh/', TokenRefreshView.as_view(), name='user_token_refresh'),
]

password_reset_urls = [
     path('forgot-my-password/', forgot_my_password, name="user_forgot_my_password"),
     path('forgot-my-password/<str:uidb64>/<str:token>', modify_forgotten_password, name="user_modify_password"),
]

extra_urls = [
     path('users/', get_all_users, name='user_list'),
     path('contact/', contact_support_email, name="support_contact"),
]

urlpatterns = register_urls + login_urls + password_reset_urls + extra_urls