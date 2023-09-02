from django.contrib import admin

from ..models.access import Access


class AccessAdmin(admin.ModelAdmin):
    list_display = (
        "material_id",
        "user_id",
        "views",
        "last_view",
        "completed",
        "like",
    )


admin.site.register(Access, AccessAdmin)
