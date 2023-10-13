'''Module with the admin class for the IoCodeSubmission model'''
from django.contrib import admin
from ..models.io_code_submission import IoCodeSubmission


class IoCodeSubmissionAdmin(admin.ModelAdmin):
    '''Class that defines the admin interface for the IoCodeSubmission model'''
    
    list_display = (
        "material_id",
        "response_char",
        "execution_time",
        "execution_memory",
        "completion_rate",
    )


admin.site.register(IoCodeSubmission, IoCodeSubmissionAdmin)
