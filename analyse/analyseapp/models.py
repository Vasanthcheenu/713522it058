from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    post_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]  # Show first 50 chars
