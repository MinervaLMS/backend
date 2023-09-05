# Generated by Django 4.2.4 on 2023-09-05 02:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_enrollment_appraisal_stars"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enrollment",
            name="appraisal_stars",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(10),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
    ]
