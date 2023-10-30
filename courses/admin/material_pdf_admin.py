from django.contrib import admin

from ..models.material_pdf import MaterialPDF


class MaterialPDFAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "material_id",
    )


admin.site.register(MaterialPDF, MaterialPDFAdmin)
