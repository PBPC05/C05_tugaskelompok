from django.db import models
from django.contrib.auth.models import User
import datetime

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

    def increment_likes(self):
        self.forums_likes += 1
        self.save()
    
    def increment_replies_counts(self):
        self.forums_replies_counts += 1
        self.save()

    def is_hot_True(self):
        self.is_hot = True
        self.save()

    def is_hot_False(self):
        self.is_hot = False
        self.save()

    def get_duration_since_created(self):
        datetimenow = datetime.datetime.now()
        return self.created_at - datetimenow

class ForumsReplies(models.Model):
    forums_id = models.ForeignKey(Forums, on_delete=models.CASCADE, related_name="replies")
    # user
    replies_content = models.TextField()
    forums_replies_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()
    