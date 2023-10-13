from django.db import models

from .module import Module


class Material(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, blank=False)
    material_type = models.CharField(max_length=3, blank=False)
    is_extra = models.BooleanField(default=False, blank=False)
    order = models.IntegerField(blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)

    # Many-to-many relationship
    comments = models.ManyToManyField(
        "accounts.User",
        through="social.Comment",
        through_fields=("material_id", "user_id"),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # There's only one material in that order for that module
                fields=["order", "module_id"],
                name="unique_order_module",
            ),
        ]

    def save(self, *args, **kwargs):
        if self.order is None:
            # In material creation, automatically assign the next possible order
            try:
                self.order = (
                    Material.objects.filter(module_id=self.module_id).aggregate(
                        models.Max("order")
                    )["order__max"]
                    + 1
                )
            except Exception:
                self.order = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module_id} - {self.name}"
