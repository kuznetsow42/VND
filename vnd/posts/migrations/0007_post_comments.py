# Generated by Django 4.2.6 on 2023-12-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_comment_options_alter_comment_image_and_more'),
        ('posts', '0006_alter_post_bookmarks_alter_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, to='comments.comment'),
        ),
    ]
