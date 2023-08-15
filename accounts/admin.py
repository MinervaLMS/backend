from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    """
    Class to customize the user administration panel
    """
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("id" ,"email", "first_name", "last_name", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active",)
    fieldsets = (
        ("Information", {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","first_name", "last_name", "password1", "password2",
                "is_staff", "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("id",)

# Register your models here.
admin.site.register(User, CustomUserAdmin)