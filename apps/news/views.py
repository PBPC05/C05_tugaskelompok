from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from apps.news.models import News
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
def show_main(request):
    context = {
        'news_list': News.objects.all()
    }
    return render(request, "news_main.html", context)

def show_news_detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, 'news_detail.html', context)

def show_news_create(request):
    return render(request, "news_create.html")

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
    )
    news.save()

    response = redirect('news_main.html')
    response.status_code = 201
    return response 


def show_news_edit(request, news_id):
    context = {
        'news_id': news_id
    }

    return render(request, "news_edit.html", context)

@require_POST
def edit_news_ajax(request, news_id):
    edited_data = {
        'title': strip_tags(request.POST.get("title")),
        'content': strip_tags(request.POST.get("content")),
        'category': request.POST.get("category"),
        'thumbnail': request.POST.get("thumbnail"),
        'is_featured': request.POST.get("is_featured") == "on",
    }

    News.objects.filter(pk=news_id).update(**edited_data)

    response = redirect('news:show_main')
    response.status_code = 301
    return response 

def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    return HttpResponseRedirect(reverse('news:show_main'))

def show_json(request):
    news_list = News.objects.all()
    data = [
        {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
        }
        for news in news_list
    ]

    return JsonResponse(data, safe=False)

def show_json_by_id(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        data = {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
        }
        return JsonResponse(data)
    except News.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
