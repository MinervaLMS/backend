from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    alias = models.CharField(max_length=20, blank=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.alias


class Module(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, blank=False)
    order = models.IntegerField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # There's only one module in that order for that course
                fields=['order', 'course_id'], name='unique_order_course'),
            models.UniqueConstraint(
                # There's only one module with that name for that course
                fields=['name', 'course_id'], name='unique_name_course'),
        ]

    def __str__(self):
        return f'{self.course_id}: {self.name}'


class Material(models.Model):
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, blank=False)
    material_type = models.CharField(max_length=3, blank=False)
    is_extra = models.BooleanField(default=False, blank=False)
    order = models.IntegerField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # There's only one material in that order for that module
                fields=['order', 'module_id'], name='unique_order_module'),
        ]

    def __str__(self):
        return self.name
