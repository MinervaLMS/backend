# Generated by Django 4.2.4 on 2023-08-17 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_id_alter_material_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='order',
            field=models.IntegerField(),
        ),
    ]
