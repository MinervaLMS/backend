from django.contrib import admin

from ..models.course import Course
from .module_admin import ModuleInline


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "alias",
    )
    search_fields = ("name", "alias")
    inlines = [ModuleInline]


admin.site.register(Course, CourseAdmin)
