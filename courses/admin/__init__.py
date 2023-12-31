from .course_admin import CourseAdmin
from .module_admin import ModuleAdmin
from .material_admin import MaterialAdmin
from .material_html_admin import MaterialHTMLAdmin
from .material_video_admin import MaterialVideoAdmin
from .material_pdf_admin import MaterialPDFAdmin
from .enrollment_admin import EnrollmentAdmin
from .access_admin import AccessAdmin
from ioc.admin.material_io_code_admin import MaterialIoCodeAdmin
from .instructor_admin import InstructorAdmin

_ = [
    CourseAdmin,
    ModuleAdmin,
    MaterialAdmin,
    MaterialHTMLAdmin,
    MaterialVideoAdmin,
    MaterialPDFAdmin,
    EnrollmentAdmin,
    AccessAdmin,
    MaterialIoCodeAdmin,
    InstructorAdmin,
]
