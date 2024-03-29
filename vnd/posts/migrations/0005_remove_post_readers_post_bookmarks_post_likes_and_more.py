# Generated by Django 4.2.6 on 2023-12-01 08:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_rename_is_bookmarked_userpostrelation_bookmark_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='readers',
        ),
        migrations.AddField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmarked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserPostRelation',
        ),
    ]
