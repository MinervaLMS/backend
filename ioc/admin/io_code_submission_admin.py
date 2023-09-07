from django.contrib import admin
from ..models.io_code_submission import IoCodeSubmission


class IoCodeSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "material_id",
        "response_char",
        "execution_time",
        "execution_memory",
        "completion_rate",
    )


admin.site.register(IoCodeSubmission, IoCodeSubmissionAdmin)
