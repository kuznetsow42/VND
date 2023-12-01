from django.contrib import admin

from posts.models import Post, Category, Image

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Image)
