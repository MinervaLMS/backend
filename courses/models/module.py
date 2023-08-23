from django.db import models

from .course import Course

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