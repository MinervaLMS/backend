from django.contrib import admin

from ..models import MaterialVideo


class MaterialVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_id', 'length', 'external_id', 'source')
    list_filter = ('material_id', 'external_id')
    search_fields = ('material_id', 'external_id')


class MaterialVieoInline(admin.StackedInline):
    model = MaterialVideo
    extra = 1


admin.site.register(MaterialVideo, MaterialVideoAdmin)
