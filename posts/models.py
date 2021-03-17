from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import *


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/',
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Post_set')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.Comments_set.all().count()

    class Meta:
        ordering = ('-created',)


class Comments(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='Comments_set')
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('like', 'like'),
    ('unlike', 'unlike'),
)


class Likes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likee')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=8, choices=LIKE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user}-{self.post}-{self.value}")
