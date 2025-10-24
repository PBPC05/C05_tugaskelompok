from django.shortcuts import render
from apps.forums.models import Forums
from apps.news.models import News

def home_view(request):
    featured_articles = News.objects.filter(is_featured=True).order_by('-created_at')[:4]
    latest_forums = Forums.objects.all().order_by('-created_at')[:6]

    context = {
        "featured_articles": featured_articles,
        "latest_forums": latest_forums,
    }
    return render(request, "home.html", context)
