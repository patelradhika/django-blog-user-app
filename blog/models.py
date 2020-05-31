from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'profile_images', default = 'profile_images/default_pic.png')

    
class BlogPost(models.Model):

    __tablename__ = 'blogpost'

    title = models.CharField(max_length=140)
    content = models.TextField()
    written_on = models.DateTimeField(default=timezone.now)
    posted_on = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def approved_comments(self):
        return self.comments.filter(approved=True)

    def unapproved_comments(self):
        return self.comments.filter(approved=False)

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.comment