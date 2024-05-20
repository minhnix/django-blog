from django.db import models
from martor.models import MartorField
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = MartorField(null=True, blank=True)
    url = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(upload_to="thumbnail/", null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", related_name="posts")
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class User(AbstractUser):
    def __str__(self):
        return self.username
    

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    def __str__(self):
        return self.content[:50]