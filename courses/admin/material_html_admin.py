from django.contrib import admin

from ..models.material_html import MaterialHTML


class MaterialHTMLAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "material_id",
    )


admin.site.register(MaterialHTML, MaterialHTMLAdmin)
