from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Forums(models.Model):
    forums_id = models.UUIDField(auto_created=True, primary_key=True)
    # user
    title = models.CharField(max_length=255)
    content = models.TextField()
    forums_views = models.PositiveIntegerField(default=0)
    forums_likes = models.PositiveIntegerField(default=0)
    forums_replies_counts = models.PositiveIntegerField(default=0)
    is_hot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.forums_views += 1
        self.save()

class ForumsReplies(models.Model):
    forums_id = models.ForeignKey(Forums, on_delete=models.CASCADE, related_name="forums")
    # user
    replies_content = models.TextField()
    forums_replies_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()
    