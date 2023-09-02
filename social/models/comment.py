from django.db import models


class Comment(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    material_id = models.ForeignKey("courses.Material", on_delete=models.CASCADE)
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    parent_comment_id = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    content = models.TextField()
    fixed = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"user {self.user_id} commented the material {self.material_id}"
