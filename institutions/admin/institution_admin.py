from django.contrib import admin

from ..models.institution import Institution


class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "alias",
        "description",
    )
    search_fields = ("name", "alias")
    inlines = []


admin.site.register(Institution, InstitutionAdmin)
