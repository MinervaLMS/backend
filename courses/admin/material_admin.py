from django.contrib import admin

from ..models.material import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "material_type",
        "module_id",
        "is_extra",
    )
    list_filter = ("material_type",)
    search_fields = ("name", "module_id")


class MaterialInline(admin.StackedInline):
    model = Material
    extra = 1


admin.site.register(Material, MaterialAdmin)
