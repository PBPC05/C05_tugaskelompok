from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from apps.news.models import News, Comment
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

import uuid

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

@login_required(login_url="/auth/login/")
def show_news_create(request):
    return render(request, "news_create.html")

@require_POST
@login_required(login_url="/auth/login/")
def create_news(request):
    title = strip_tags(request.POST.get("title"))
    content = strip_tags(request.POST.get("content"))
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == "on"
    user = request.user

    news = News(
        user = user,
        title = title,
        content = content,
        category = category,
        thumbnail = thumbnail,
        is_featured = is_featured,
    )
    news.save()

    response = redirect('news_main.html')
    return response 

@login_required(login_url="/auth/login/")
def show_news_edit(request, news_id):
    context = {
        'news_id': news_id
    }

    return render(request, "news_edit.html", context)

@require_POST
@login_required(login_url="/auth/login/")
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
    return response 

@login_required(login_url="/auth/login/")
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    return HttpResponseRedirect(reverse('news:show_main'))

def show_json(request):
    try:
        news_list = News.objects.all()
        data = [
            {
                'username': news.user.username if news.user else 'Anonymous',
                'id': str(news.id),
                'title': news.title,
                'content': news.content,
                'category': news.category,
                'thumbnail': news.thumbnail,
                'news_views': news.news_views,
                'news_comments': news.news_comments,
                'created_at': news.created_at.isoformat() if news.created_at else None,
                'is_featured': news.is_featured,
            }
            for news in news_list
        ]

        return JsonResponse(data, safe=False)
    except Exception as e:
        print("Error")

def show_json_by_id(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        data = {
            'username': news.user.username if news.user else 'Anonymous',
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'news_comments': news.news_comments,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
        }
        return JsonResponse(data)
    except News.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
@require_POST
@login_required(login_url="/auth/login/")
def post_comment(request, news_id):
    comment_news = get_object_or_404(News, pk=news_id)
    comment_news.increment_comments()
    content = request.POST.get("comment-body")

    comment = Comment(
        user = request.user,
        news = comment_news,
        content = content
    )
    comment.save()

    response = redirect('news:show_news_detail', news_id=news_id)
    return response 

def get_comments_json(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = Comment.objects.filter(news_id=news).order_by("-created_at")

    data = [
        {
            # validasi UUID tapi fallback ke string biasa
            "id": str(uuid.UUID(str(comment.id))) if isinstance(comment.id, uuid.UUID) or str(comment.id).count('-') == 4 else str(comment.id),
            "username": getattr(comment, "username", None) or (
                comment.user.username if comment.user else "Anonymous"
            ),
            "content": getattr(comment, "body", "") or getattr(comment, "content", ""),
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for comment in comments
    ]
    print(data)

    return JsonResponse(data, safe=False)

def delete_comment(request, comment_id, news_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    response = redirect('news:show_news_detail', news_id=news_id)
    return response
