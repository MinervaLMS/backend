# Generated by Django 4.2.4 on 2023-09-01 18:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0014_alter_materialhtml_material_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="material",
            name="comments",
            field=models.ManyToManyField(
                through="social.Comment", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="material",
            name="dislikes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="material",
            name="likes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="material",
            name="total_comments",
            field=models.IntegerField(default=0),
        ),
    ]
