# Generated by Django 4.2.4 on 2023-08-17 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_course_alias_alter_course_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RunSQL("ALTER SEQUENCE courses_course_id_seq RESTART WITH 1000;"),
        migrations.AlterField(
            model_name='material',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RunSQL("ALTER SEQUENCE courses_material_id_seq RESTART WITH 1000;"),
        migrations.AlterField(
            model_name='material',
            name='order',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RunSQL("ALTER SEQUENCE courses_module_id_seq RESTART WITH 1000;"),
    ]