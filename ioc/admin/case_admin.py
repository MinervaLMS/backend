"""Module for case admin"""

from django.contrib import admin

from ..models.case import Case


class CaseAdmin(admin.ModelAdmin):
    """Class that defines the admin interface for the Case model"""

    list_display = ("input", "output", "material_io_code_id", "id_case")


admin.site.register(Case, CaseAdmin)
