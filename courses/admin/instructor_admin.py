from django.contrib import admin

from ..models.instructor import Instructor


class InstructorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "course_id",
        "instructor_type",
    )


admin.site.register(Instructor, InstructorAdmin)
