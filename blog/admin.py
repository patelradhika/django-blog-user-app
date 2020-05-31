from django.contrib import admin
from .models import BlogPost, UserImage, Comments

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(UserImage)
admin.site.register(Comments)