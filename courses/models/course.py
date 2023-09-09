from django.db import models


class Course(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    name = models.CharField(max_length=100, blank=False, unique=True)
    alias = models.CharField(max_length=20, blank=False, unique=True)
    description = models.TextField(blank=True)
    course_instructional_materials = models.IntegerField(default=0)
    course_assessment_materials = models.IntegerField(default=0)
    course_extra_materials = models.IntegerField(default=0)
    min_assessment_progress = models.IntegerField(default=70)
    average_stars = models.IntegerField(null=True, blank=True)
    appraisals = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    institution = models.ForeignKey(
        "institutions.Institution", on_delete=models.CASCADE, blank=False, null=False
    )
    parent_course = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    enrollments = models.ManyToManyField("accounts.User", through="Enrollment")

    def __str__(self):
        return self.alias
