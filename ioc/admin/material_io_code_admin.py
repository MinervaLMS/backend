from django.contrib import admin

from ..models.material_io_code import MaterialIoCode


class MaterialIoCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "material_id", "max_time", "max_memory", "isActive")
    list_filter = ("material_id", "id")
    search_fields = ("material_id", "id")


class MaterialIoCodeInline(admin.StackedInline):
    model = MaterialIoCode
    extra = 1


admin.site.register(MaterialIoCode, MaterialIoCodeAdmin)
