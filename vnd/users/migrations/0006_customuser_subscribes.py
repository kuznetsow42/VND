# Generated by Django 4.2.6 on 2023-12-06 15:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_delete_engine_alter_customuser_favorite_engines_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subscribes',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
