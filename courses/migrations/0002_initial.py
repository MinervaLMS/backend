# Generated by Django 4.2.4 on 2023-09-09 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('institutions', '0001_initial'),
        ('social', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='comments',
            field=models.ManyToManyField(through='social.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='module_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.module'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='enrollments',
            field=models.ManyToManyField(through='courses.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution'),
        ),
        migrations.AddField(
            model_name='course',
            name='parent_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='access',
            name='material_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.material'),
        ),
        migrations.AddField(
            model_name='access',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='module',
            constraint=models.UniqueConstraint(fields=('order', 'course_id'), name='unique_order_course'),
        ),
        migrations.AddConstraint(
            model_name='module',
            constraint=models.UniqueConstraint(fields=('name', 'course_id'), name='unique_name_course'),
        ),
        migrations.AddConstraint(
            model_name='material',
            constraint=models.UniqueConstraint(fields=('order', 'module_id'), name='unique_order_module'),
        ),
        migrations.AddConstraint(
            model_name='enrollment',
            constraint=models.UniqueConstraint(fields=('user_id', 'course_id'), name='unique_enrollment'),
        ),
        migrations.AddConstraint(
            model_name='access',
            constraint=models.UniqueConstraint(fields=('material_id', 'user_id'), name='unique_access'),
        ),
    ]
