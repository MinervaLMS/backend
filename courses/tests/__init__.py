from .course_tests import (
    CreateCourseTestCase,
    GetCourseTestCase,
    UpdateCourseTestCase,
    DeleteCourseTestCase,
)
from .module_tests import (
    CreateModuleTestCase,
    GetModuleTestCase,
    UpdateModuleTestCase,
    DeleteModuleTestCase,
    GetMaterialByModuleTestCase,
    UpdateMaterialOrderTestCase,
)
from .material_tests import (
    CreateMaterialTestCase,
    GetMaterialTestCase,
    UpdateMaterialTestCase,
    DeleteMaterialTestCase,
)
from .material_html_tests import (
    CreateMaterialHTMLTestCase,
    GetMaterialHTMLTestCase,
    UpdateMaterialHTMLTestCase,
    DeleteMaterialHTMLTestCase,
)
from .material_video_tests import (
    CreateMaterialVideoTestCase,
    GetMaterialVideoTestCase,
    UpdateMaterialVideoTestCase,
    DeleteMaterialVideoTestCase,
)
from .enrollment_tests import AppraiseCourseTestCase

_ = [
    CreateCourseTestCase,
    GetCourseTestCase,
    UpdateCourseTestCase,
    DeleteCourseTestCase,
]
_ = [
    CreateModuleTestCase,
    GetModuleTestCase,
    UpdateModuleTestCase,
    DeleteModuleTestCase,
    GetMaterialByModuleTestCase,
    UpdateMaterialOrderTestCase,
]
_ = [
    CreateMaterialTestCase,
    GetMaterialTestCase,
    UpdateMaterialTestCase,
    DeleteMaterialTestCase,
]
_ = [
    CreateMaterialHTMLTestCase,
    GetMaterialHTMLTestCase,
    UpdateMaterialHTMLTestCase,
    DeleteMaterialHTMLTestCase,
]
_ = [
    CreateMaterialVideoTestCase,
    GetMaterialVideoTestCase,
    UpdateMaterialVideoTestCase,
    DeleteMaterialVideoTestCase,
]

_ = [AppraiseCourseTestCase]
