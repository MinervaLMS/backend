# Generated by Django 4.2.4 on 2023-09-02 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0015_merge_20230901_1032"),
    ]

    operations = [
        migrations.CreateModel(
            name="Access",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("views", models.IntegerField(default=1)),
                ("last_view", models.DateTimeField(auto_now=True)),
                ("completed", models.BooleanField(blank=True, null=True)),
                ("like", models.BooleanField(blank=True, null=True)),
                (
                    "material_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.material",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="access",
            constraint=models.UniqueConstraint(
                fields=("material_id", "user_id"), name="unique_access"
            ),
        ),
    ]