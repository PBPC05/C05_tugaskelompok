from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.utils import timezone

from .models import Forums, ForumsReplies
from .forms import ForumsForm, ForumsRepliesForm

def forums_list_view(request):

    return render(request, "forums/list.html", {})

def forums_list_json(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))

    qs = Forums.objects.all().order_by('-created_at')

    if q:
        qs = qs.filter(title__icontains=q)

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    items = []
    for forum in page_obj.object_list:
        items.append({
            "id": str(forum.forums_id),
            "title": forum.title,
            "content": forum.content[:350],
            "thumbnail": None,
            "category": "forum",
            "created_at": forum.created_at.isoformat(),
            "news_views": forum.forums_views,
            "news_comments": forum.forums_replies_counts,
            "is_featured": forum.is_hot,
            "author": forum.user.username if forum.user else None,
        })

    return JsonResponse({
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "page": page_obj.number,
        "results": items,
    })

def forum_detail_view(request, pk):
    forum = get_object_or_404(Forums, pk=pk)
    forum.increment_views()
    replies = forum.forum_replies.select_related('user').order_by('created_at').all()
    reply_form = ForumsRepliesForm()
    context = {
        "forum": forum,
        "replies": replies,
        "reply_form": reply_form,
    }
    return render(request, "forums/detail.html", context)

def forum_detail_json(request, pk):
    forum = get_object_or_404(Forums, pk=pk)
    replies = forum.forum_replies.order_by('created_at').all()
    items = []
    for r in replies:
        items.append({
            "id": r.id,
            "forums_id": str(r.forums_id.forums_id),
            "user": r.user.username if r.user else None,
            "replies_content": r.replies_content,
            "forums_replies_likes": r.forums_replies_likes,
            "created_at": r.created_at.isoformat(),
        })
    data = {
        "id": str(forum.forums_id),
        "title": forum.title,
        "content": forum.content,
        "forums_views": forum.forums_views,
        "forums_likes": forum.forums_likes,
        "forums_replies_counts": forum.forums_replies_counts,
        "created_at": forum.created_at.isoformat(),
        "is_hot": forum.is_hot,
        "author": forum.user.username if forum.user else None,
        "replies": items,
    }
    return JsonResponse(data)

@login_required
def forums_create_view(request):
    if request.method == "POST":
        form = ForumsForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('forums:show_forum_detail', pk=obj.forums_id)
    else:
        form = ForumsForm()
    return render(request, "forums/form.html", {"form": form, "action": "Create"})

@login_required
def forums_edit_view(request, pk):
    forum = get_object_or_404(Forums, pk=pk)
    if forum.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this forum.")
    if request.method == "POST":
        form = ForumsForm(request.POST, instance=forum)
        if form.is_valid():
            form.save()
            return redirect('forums:show_forum_detail', pk=forum.forums_id)
    else:
        form = ForumsForm(instance=forum)
    return render(request, "forums/form.html", {"form": form, "action": "Edit", "forum": forum})

@login_required
@require_POST
def forums_delete_view(request, pk):
    forum = get_object_or_404(Forums, pk=pk)
    if forum.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this forum.")
    forum.delete()
    return redirect('forums:list')

@login_required
@require_POST
def forum_like_toggle(request, pk):
    forum = get_object_or_404(Forums, pk=pk)
    action = request.POST.get('action')
    if action == 'like':
        forum.increment_likes()
    elif action == 'unlike':
        forum.decrement_likes()
    else:
        return HttpResponseBadRequest("Invalid action")
    return JsonResponse({"forums_likes": forum.forums_likes})

@login_required
@require_POST
def reply_like_toggle(request, reply_id):
    reply = get_object_or_404(ForumsReplies, pk=reply_id)
    action = request.POST.get('action')
    if action == 'like':
        reply.increment_likes()
    elif action == 'unlike':
        reply.decrement_likes()
    else:
        return HttpResponseBadRequest("Invalid action")
    return JsonResponse({"forums_replies_likes": reply.forums_replies_likes})

@login_required
@require_POST
def create_reply(request, pk):
    forum = get_object_or_404(Forums, pk=pk)
    form = ForumsRepliesForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.forums_id = forum
        reply.save()
        forum.increment_replies_counts()
        data = {
            "id": reply.id,
            "user": reply.user.username if reply.user else None,
            "replies_content": reply.replies_content,
            "created_at": reply.created_at.isoformat(),
            "forums_replies_likes": reply.forums_replies_likes
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"errors": form.errors}, status=400)

@login_required
@require_POST
def delete_reply(request, reply_id):
    reply = get_object_or_404(ForumsReplies, pk=reply_id)
    if reply.user != request.user and reply.forums_id.user != request.user:
        return HttpResponseForbidden("Not allowed to delete this reply.")
    parent = reply.forums_id
    reply.delete()
    parent.decrement_replies_counts()
    return JsonResponse({"deleted": True})
