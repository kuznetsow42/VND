# Generated by Django 4.2.6 on 2024-01-20 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0005_alter_report_reporting_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reported_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
