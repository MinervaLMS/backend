# Generated by Django 4.2.4 on 2023-10-28 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ioc", "0003_alter_iocodesubmission_completion_rate_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Case",
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
                ("id_case", models.IntegerField(null=True)),
                ("input", models.TextField()),
                ("output", models.TextField()),
                (
                    "material_io_code_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ioc.materialiocode",
                    ),
                ),
            ],
        ),
    ]
