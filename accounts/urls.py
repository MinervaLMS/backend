from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register_views,
    login_views,
    forgot_password_views,
    user_views,
    contact_support_views,
)

# TODO: Change contact/ endpoint to an independent app in the future

register_urls = [
    path("register/", register_views.user_register, name="user_register"),
    path(
        "register/confirm/<str:uidb64>/<str:token>",
        register_views.confirm_email,
        name="user_confirm_email",
    ),
    path(
        "register/resend/<str:uidb64>/",
        register_views.resend_confirmation_email,
        name="user_resend_confirmation_email",
    ),
]

login_urls = [
    path("login/", login_views.user_login, name="user_login"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="user_token_refresh"),
]

password_reset_urls = [
    path(
        "forgot-my-password/",
        forgot_password_views.forgot_my_password,
        name="user_forgot_my_password",
    ),
    path(
        "forgot-my-password/<str:uidb64>/<str:token>",
        forgot_password_views.modify_forgotten_password,
        name="user_modify_password",
    ),
]

extra_urls = [
    path("users/", user_views.get_all_users, name="user_list"),
    path("users/<int:user_id>/", user_views.get_user, name="get_user"),
    path(
        "users/<int:user_id>/courses/",
        user_views.get_user_courses,
        name="get_user_courses",
    ),
    path(
        "contact/", contact_support_views.contact_support_email, name="support_contact"
    ),
    path(
        "users/<int:user_id>/module/<int:module_id>/materials/",
        user_views.get_user_materials,
        name="get_user_materials",
    ),
    path(
        "users/<int:course_id>/<int:user_id>/modules-progress/",
        user_views.get_user_modules_progress,
        name="get_user_material",
    ),
]

urlpatterns = register_urls + login_urls + password_reset_urls + extra_urls
