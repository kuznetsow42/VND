# Generated by Django 4.2.6 on 2023-11-04 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_avatar_alter_customuser_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='links',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='links',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
        migrations.AddField(
            model_name='customuser',
            name='links',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engine',
            name='links',
            field=models.JSONField(default={'name': 'repository', 'url': 'http:/23'}),
            preserve_default=False,
        ),
    ]
