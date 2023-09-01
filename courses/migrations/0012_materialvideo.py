# Generated by Django 4.2.4 on 2023-08-31 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0011_enrollment_course_enrollments_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MaterialVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("length", models.IntegerField()),
                ("source", models.CharField(max_length=1)),
                ("external_id", models.CharField(max_length=100)),
                (
                    "material_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.material",
                    ),
                ),
            ],
        ),
    ]