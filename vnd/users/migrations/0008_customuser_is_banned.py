# Generated by Django 4.2.6 on 2024-01-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_subscribes_customuser_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
    ]