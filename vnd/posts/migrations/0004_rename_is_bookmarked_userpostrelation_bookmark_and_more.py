# Generated by Django 4.2.6 on 2023-11-12 06:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_alter_image_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpostrelation',
            old_name='is_bookmarked',
            new_name='bookmark',
        ),
        migrations.RenameField(
            model_name='userpostrelation',
            old_name='is_liked',
            new_name='like',
        ),
        migrations.AlterField(
            model_name='post',
            name='readers',
            field=models.ManyToManyField(related_name='post_relations', through='posts.UserPostRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]