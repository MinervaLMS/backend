# Generated by Django 4.2.4 on 2023-10-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0006_instructor_instructor_unique_instructor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="access",
            name="last_view",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="access",
            name="views",
            field=models.IntegerField(default=0),
        ),
    ]