from django.db import models
from django.contrib.auth.models import User
import uuid

class News(models.Model):
    CATEGORY_CHOICES = {
        'f1': 'Formula 1/FIA',
        'championship': 'Championship',
        'team': 'Team',
        'driver': 'Driver',
        'constructor': 'Constructor',
        'race': 'Race',
        'analysis': 'Analysis',
        'history': 'F1 History',
        'fanbase': 'F1 Fanbase',
        'exclusive': 'Exclusive',
        'other': 'Other',
    }

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    news_comments = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def getUrlTitle(self):
        lowerTitle = self.title.lower()
        urlTitle = lowerTitle.replace(" ", "-")
        if len(urlTitle > 255):
            return urlTitle[:255]
        else:
            return urlTitle

    @property
    def is_news_hot(self):
        return self.news_views > 200
        
    def increment_views(self):
        self.news_views += 1
        self.save()

    def increment_comments(self):
        self.news_comments += 1
        self.save()

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()