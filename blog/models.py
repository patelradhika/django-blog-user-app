from django.db import models
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):

    __tablename__ = 'blogpost'

    title = models.CharField(max_length=140)
    content = models.TextField()
    written_on = models.DateTimeField(default=timezone.now)
    posted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title