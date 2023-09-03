from django.db.models.expressions import RawSQL

from ..models.course import Course
from ..models.enrollment import Enrollment


def validate_enrollment(user_id: int, material_id: int) -> bool:
    """Verify if a user is enrolled in a course to which a material belongs.

    Args:
        user_id (int): user's id to verify if is enrolled in a course
        material_id (int): material's id to verify if its course is enrolled by user

    Returns:
        bool:
        True if user is enrolled in a course to which material belongs, False otherwise
    """
    # Query to get the course that material belongs to
    query: str = (
        "SELECT course_id_id FROM courses_module "
        "INNER JOIN courses_material ON courses_material.module_id_id "
        "= courses_module.id WHERE courses_material.id = %s"
    )
    course = Course.objects.filter(id=RawSQL(query, (material_id,))).first()
    # Verify if the user is enrolled in the course
    if Enrollment.objects.filter(user_id=user_id, course_id=course).exists():
        return True
    return False
