from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .forms import MinervaUserChangeForm, MinervaUserCreationForm

# TODO: cuando se cambie el uso de unique de username a email, cambiar todos los "username" a "email"

class MinervaUserAdmin(UserAdmin):
    """
    Class to custumize the user administration panel
    """
    add_form = MinervaUserCreationForm
    form = MinervaUserChangeForm
    model = User
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active",)
    list_filter = ("email", "first_name", "last_name", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

# Register your models here.
admin.site.register(User, MinervaUserAdmin)