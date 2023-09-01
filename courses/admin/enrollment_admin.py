from django.contrib import admin

from ..models.enrollment import Enrollment


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course_id",
        "user_id",
        "enrollment_date",
    )
    list_filter = ("course_id",)
    search_fields = ("course_id", "user_id")


admin.site.register(Enrollment, EnrollmentAdmin)
