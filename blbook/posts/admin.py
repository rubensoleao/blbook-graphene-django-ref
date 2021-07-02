from django.contrib import admin

# Register your models here.


# cookbook/ingredients/admin.py
from django.contrib import admin
from blbook.posts.models import Post

admin.site.register(Post)