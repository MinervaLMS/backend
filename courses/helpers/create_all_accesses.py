from accounts.models import User
from courses.models import Course, Access, Material, Module


def create_accesses_for_material(course_id: int, material: Material) -> None:
    """Create all accesses for all users in a course in which the material belongs

    Args:
        course_id: Course's id in which belongs all
        users that will have access to the material created
        material: Material that just has been created

    Returns:
        None

    """

    users: list[User] = Course.objects.get(id=course_id).enrollments.all()
    accesses: list[Access] = []
    for user in users:
        access: Access = Access(material_id=material, user_id=user)
        accesses.append(access)
    Access.objects.bulk_create(accesses)


def create_accesses_for_user(course: Course, user: User) -> None:
    """Create all accesses for all materials in a course for a user

    Args:
        course: Course in which belongs all materials that will be accessed to the user
        user: User that just has been enrolled in the course
    Returns:
        None
    """
    modules: list[Module] = course.module_set.all()
    materials: list[Material] = []
    for module in modules:
        materials.extend(module.material_set.all())

    accesses: list[Access] = []

    for material in materials:
        access: Access = Access(material_id=material, user_id=user)
        accesses.append(access)
    Access.objects.bulk_create(accesses)
