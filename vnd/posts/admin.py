from django.contrib import admin

from posts.models import Post, Category, UserPostRelation, Image

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(UserPostRelation)
admin.site.register(Image)
