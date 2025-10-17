from django.shortcuts import render
from django.http import HttpResponse
from apps.news.models import News
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
def show_main(request):
    context = {
        'news_list': range(5)
    }
    return render(request, "news_main.html", context)

@require_POST
def create_news(request):
    title = strip_tags(request.POST.get("title"))
    content = strip_tags(request.POST.get("content"))
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == "on"
    user = request.user

    news = News(
        title = title,
        content = content,
        category = category,
        thumbnail = thumbnail,
        is_featured = is_featured,
        user = user
    )
    news.save()

    return HttpResponse(b"CREATED", status=201)    

def show_news_create(request):
    return render(request, "news_create.html")
