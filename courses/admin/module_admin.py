from django.contrib import admin

from ..models import Module
from .material_admin import MaterialInline


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course_id',)
    list_filter = ('course_id',)
    search_fields = ('name', 'course__name')
    inlines = [MaterialInline]


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


admin.site.register(Module, ModuleAdmin)
