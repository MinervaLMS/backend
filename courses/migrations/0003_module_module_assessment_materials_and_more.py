# Generated by Django 4.2.4 on 2023-09-08 01:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="module",
            name="module_assessment_materials",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="module",
            name="module_extra_materials",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="module",
            name="module_instructional_materials",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="module",
            name="module_total_materials",
            field=models.IntegerField(default=0),
        ),
    ]
