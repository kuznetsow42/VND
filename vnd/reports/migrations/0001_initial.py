# Generated by Django 4.2.6 on 2023-12-24 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('top_priority', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.PositiveIntegerField()),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('content_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.reason')),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
