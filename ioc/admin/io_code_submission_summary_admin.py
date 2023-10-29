from django.contrib import admin

from ..models.io_code_submission_summary import IoCodeSubmissionSummary


class IoCodeSubmissionSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "material",
        "user",
        "attempts",
        "hits",
        "points",
        "min_execution_time",
        "min_execution_memory",
        "max_completion_rate",
    )


admin.site.register(IoCodeSubmissionSummary, IoCodeSubmissionSummaryAdmin)
