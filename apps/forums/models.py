from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

# Create your models here.
class Forums(models.Model):
    forums_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    forums_views = models.PositiveIntegerField(default=0)
    forums_likes = models.ManyToManyField(User, related_name="liked_forums", blank=True)
    forums_replies_counts = models.PositiveIntegerField(default=0)
    is_hot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def increment_views(self):
        self.forums_views += 1
        self.save()

    def user_has_liked(self, user):
        return self.forums_likes.filter(id=user.id).exists()
    
    def get_duration_since_created(self):
        return self.created_at - timezone.now()

class ForumsReplies(models.Model):
    forums = models.ForeignKey(Forums, on_delete=models.CASCADE, related_name="forum_replies")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    replies_content = models.TextField()
    forums_replies_likes = models.ManyToManyField(User, related_name="liked_replies", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.replies_content

    def user_has_liked(self, user):
        return self.forums_replies_likes.filter(id=user.id).exists()

    def get_duration_since_created(self):
        return self.created_at - timezone.now()
    
class ForumView(models.Model):
    forum = models.ForeignKey(Forums, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('forum', 'user') 

    def __str__(self):
        return f"{self.user.username} viewed {self.forum.title}"