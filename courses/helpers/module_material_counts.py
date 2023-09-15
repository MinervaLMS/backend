from ..serializers.material_serializer import MaterialSerializer
from ..models.material import Material
from ..models.module import Module
from ..models.access import Access
from ..models.module_progress import Module_progress
from accounts.models.user import User


def update_count_created_material(*, serializer: MaterialSerializer) -> None:
    """
    Adds the created material to the respective module's material count.
    Keyword args:
        serializer (MaterialSerializer): serializer with the material data.
    Returns:
        None

    """
    module: Module = serializer.validated_data["module_id"]

    if serializer.validated_data["is_extra"]:
        # Is extra material
        module.module_extra_materials += 1

    elif serializer.validated_data["material_type"] == "ioc":
        # Is assessment material
        module.module_assessment_materials += 1

    else:
        # Is instructional material
        module.module_instructional_materials += 1

    module.module_total_materials = (
            module.module_extra_materials
            + module.module_assessment_materials
            + module.module_instructional_materials
    )
    module.save()


def update_count_updated_material(
        *,
        material: Material,
        old_material_type: str,
        old_is_extra: bool,
        new_material_type: str | None,
        new_is_extra: str | None,
) -> None:
    """
    Updates the material count when a material is updated for the respective module
    of the material.
    Keyword args:
        material (Material): Material from where to get the module to update.
        old_material_type (str): The material type currently in the database.
        old_is_extra (bool): The is_extra value currently in the database.
        new_material_type (str | None): The material type received in the request.
        new_is_extra (str | None): The is_extra value received in the request.
    Returns:
        None
    """
    module: Module = material.module_id

    # As the fields is_extra and material_type are not required,
    # we need to check if they are
    # not None before updating the module's material counts

    if new_is_extra is not None:
        # Guaranteed is_extra is either "True" or "False".
        # As it is a string, we need to convert it to a boolean
        new_is_extra = (
            True if (new_is_extra == "True" or new_is_extra ==
                     "true") else False
        )

        if not old_is_extra and new_is_extra:
            # is_extra changed from False to True
            module.module_extra_materials += 1

            # Either was an assessment material or not
            if old_material_type == "ioc":
                # Was an assessment material
                module.module_assessment_materials -= 1
            else:
                # Was an instructional material
                module.module_instructional_materials -= 1

        elif old_is_extra and not new_is_extra:
            # is_extra changed from True to False
            module.module_extra_materials -= 1
            if new_material_type is not None:
                # We received the new material_type, check the type
                if old_material_type == "ioc" and new_material_type != "ioc":
                    # old material was an assessment material and new material is not
                    module.module_instructional_materials += 1

                elif new_material_type == "ioc" and old_material_type != "ioc":
                    # old material was an instructional material and new material is not
                    module.module_assessment_materials += 1
                else:
                    # old material and new material are different
                    # instructional materials.
                    module.module_instructional_materials += 1

            elif old_material_type == "ioc":
                # We did not receive the new material_type,
                # but the old material was an assessment material
                module.module_assessment_materials += 1
            else:
                # We did not receive the new material_type,
                # but the old material was an instructional material
                module.module_instructional_materials += 1

    elif not old_is_extra:
        if new_material_type is not None:
            # Guaranteed material was not extra material before
            # and material_type was received
            if old_material_type == "ioc" and new_material_type != "ioc":
                # old material was an assessment material and new material is not
                module.module_assessment_materials -= 1
                module.module_instructional_materials += 1

            elif new_material_type == "ioc" and old_material_type != "ioc":
                # old material was an instructional material and new material is not
                module.module_assessment_materials += 1
                module.module_instructional_materials -= 1

    module.module_total_materials = (
            module.module_extra_materials
            + module.module_assessment_materials
            + module.module_instructional_materials
    )

    module.save()


def update_count_deleted_material(*, material: Material) -> None:
    """
    Subtracts the deleted material from the respective module's material count.

    Keyword args:
        material (Material): Material from where to get the module to update.
    Returns:
        None

    """
    module: Module = material.module_id
    access_list: list[Access] = Access.objects.filter(material_id=material.id, completed=True)
    user_id: User | None = None
    module_progress: Module_progress | None = None
    for access in access_list:
        if user_id != access.user_id:
            user_id = access.user_id
            module_progress: Module_progress = Module_progress.objects.get(
                user_id=user_id, module_id=module.id
            )
        if material.material_type == "ioc" and material.is_extra is False:
            # Is assessment material
            module_progress.module_assessment_progress -= 1
        elif material.is_extra is False:
            # Is instructional material
            module_progress.module_instructional_progress -= 1

        module_progress.save()
    if material.is_extra and module.module_extra_materials > 0:
        # Is extra material
        module.module_extra_materials -= 1

    elif material.material_type == "ioc" and module.module_assessment_materials > 0:
        # Is assessment material
        module.module_assessment_materials -= 1

    elif module.module_instructional_materials > 0:
        # Is instructional material
        module.module_instructional_materials -= 1

    module.module_total_materials = (
            module.module_extra_materials
            + module.module_assessment_materials
            + module.module_instructional_materials
    )
    module.save()
