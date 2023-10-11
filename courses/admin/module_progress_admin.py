from django.contrib import admin

from ..models.module_progress import Module_progress


class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "module_id",
        "module_instructional_progress",
        "module_assessment_progress",
    )


admin.site.register(Module_progress, ModuleProgressAdmin)
