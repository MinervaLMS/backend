# Generated by Django 4.2.4 on 2023-10-10 17:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ioc", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="iocodesubmission",
            name="char_check",
        ),
        migrations.AddField(
            model_name="iocodesubmission",
            name="code",
            field=models.CharField(default="print()"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="iocodesubmission",
            name="language",
            field=models.CharField(default="py3", max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="iocodesubmission",
            name="response_char",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name="iocodesubmission",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "response_char__in",
                        {"M", "I", "P", "J", "T", "E", "C", "A", "W"},
                    ),
                    ("response_char__isnull", True),
                    _connector="OR",
                ),
                name="char_check",
            ),
        ),
    ]
