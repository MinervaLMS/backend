from django.db import models

# TODO: Complete all courses related models with the rest of the fields and constraints needed


class Course(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID', editable=False)
    name = models.CharField(max_length=100, blank=False, unique=True)
    alias = models.CharField(max_length=20, blank=False, unique=True)
    description = models.TextField(blank=True)

    enrollments = models.ManyToManyField("accounts.User", through='Enrollment')

    def __str__(self):
        return self.alias


class Module(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID', editable=False)
    course_id = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, blank=False)
    order = models.IntegerField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # There's only one module in that order for that course
                fields=['order', 'course_id'], name='unique_order_course'),
            models.UniqueConstraint(
                # There's only one module with that name for that course
                fields=['name', 'course_id'], name='unique_name_course'),
        ]

    def save(self, *args, **kwargs):
        if not self.order:
            # In module creation, automatically assign the next possible order
            try:
                self.order = Module.objects.filter(course_id=self.course_id).aggregate(
                    models.Max('order'))['order__max'] + 1
            except Exception:
                self.order = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course_id}: {self.name}'


class Material(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID', editable=False)
    module_id = models.ForeignKey(
        Module, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, blank=False)
    material_type = models.CharField(max_length=3, blank=False)
    is_extra = models.BooleanField(default=False, blank=False)
    order = models.IntegerField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # There's only one material in that order for that module
                fields=['order', 'module_id'], name='unique_order_module'),
        ]

    def save(self, *args, **kwargs):
        if not self.order:
            # In material creation, automatically assign the next possible order
            try:
                self.order = Material.objects.filter(module_id=self.module_id).aggregate(
                    models.Max('order'))['order__max'] + 1
            except Exception:
                self.order = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.module_id}: {self.name}'


class Enrollment(models.Model):
    user_id = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, blank=False)
    course_id = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=False)
    enrollment_date = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # (user_id, course_id) pair is the primary key or the enrollment
                fields=['user_id', 'course_id'], name='unique_enrollment'),
        ]

    def __str__(self):
        return f'{self.user_id} enrollment in course {self.course_id}'
