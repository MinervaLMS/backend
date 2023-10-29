# Generated by Django 4.2.4 on 2023-10-29 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0007_alter_access_last_view_alter_access_views'),
        ('ioc', '0004_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialiocode',
            name='max_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='materialiocode',
            name='min_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='materialiocode',
            name='points_penalty',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='IoCodeSubmissionSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts', models.IntegerField(default=1)),
                ('hits', models.IntegerField()),
                ('points', models.IntegerField()),
                ('min_execution_time', models.IntegerField()),
                ('min_execution_memory', models.IntegerField()),
                ('max_completion_rate', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission_summary', to='courses.material')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission_summary', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='iocodesubmissionsummary',
            constraint=models.UniqueConstraint(fields=('user', 'material'), name='unique_io_code_submission_summary'),
        ),
    ]
