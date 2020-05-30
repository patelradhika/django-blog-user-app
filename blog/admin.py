from django.contrib import admin
from .models import BlogPost, UserImage

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(UserImage)