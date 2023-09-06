from rest_framework import serializers

from ..models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "alias",
            "description",
            "course_instructional_materials",
            "course_assessment_materials",
            "course_extra_materials",
            "min_assessment_progress",
            "average_stars",
            "appraisals",
            "comments",
            "parent_course_id",
            "enrollments",
            "institution_id"
        ]
