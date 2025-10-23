from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Forums, ForumsReplies, ForumView
from .forms import ForumsForm, ForumsRepliesForm

def forums_list_view(request):
    return render(request, "forums/list.html", {})

def forums_list_json(request):
    q = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 9))
    filter_type = request.GET.get("filter", "latest")

    qs = Forums.objects.all()

    if q:
        qs = qs.filter(title__icontains=q)

    if filter_type == "latest":
        qs = qs.order_by("-created_at")
    elif filter_type == "oldest":
        qs = qs.order_by("created_at")
    elif filter_type == "hot":
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        qs = qs.filter(created_at__gte=one_week_ago).order_by("-forums_views")

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    items = [
        {
            "id": str(f.forums_id),
            "title": f.title,
            "content": f.content[:350],
            "created_at": f.created_at.isoformat(),
            "forums_views": f.forums_views,
            "forums_replies_counts": f.forums_replies_counts,
            "is_featured": f.is_hot,
            "author": f.user.username if f.user else None,
        }
        for f in page_obj.object_list
    ]

    return JsonResponse(
        {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "page": page_obj.number,
            "results": items,
        }
    )

def forum_detail_view(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)

    if request.user.is_authenticated:
        viewed, created = ForumView.objects.get_or_create(forum=forum, user=request.user)
        if created:
            forum.forums_views += 1
            forum.save(update_fields=["forums_views"])
    else:
        session_key = f"viewed_forum_{forum.forums_id}"
        if not request.session.get(session_key, False):
            forum.forums_views += 1
            forum.save(update_fields=["forums_views"])
            request.session[session_key] = True

    user_has_liked = (
        forum.user_has_liked(request.user)
        if request.user.is_authenticated
        else False
    )

    replies = forum.forum_replies.order_by("-created_at")[:5]

    if request.user.is_authenticated:
        for r in replies:
            r.user_has_liked = r.user_has_liked(request.user)
    else:
        for r in replies:
            r.user_has_liked = False


    context = {
        "forum": forum,
        "replies": replies,
        "reply_form": ForumsRepliesForm(),
        "user_has_liked": user_has_liked,
    }

    return render(request, "forums/detail.html", context)


def forum_detail_json(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    replies = forum.forum_replies.order_by("created_at").all()

    items = [
        {
            "id": r.id,
            "forum_id": str(r.forums.forums_id),
            "user": r.user.username if r.user else None,
            "replies_content": r.replies_content,
            "likes_count": r.forums_replies_likes.count(),
            "created_at": r.created_at.isoformat(),
        }
        for r in replies
    ]

    data = {
        "id": str(forum.forums_id),
        "title": forum.title,
        "content": forum.content,
        "forums_views": forum.forums_views,
        "forums_likes": forum.forums_likes.count(),
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
            return redirect("forums:show_forum_detail", pk=obj.forums_id)
    else:
        form = ForumsForm()
    return render(request, "forums/form.html", {"form": form, "action": "Create"})


@login_required
def forums_edit_view(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    if forum.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this forum.")

    if request.method == "POST":
        form = ForumsForm(request.POST, instance=forum)
        if form.is_valid():
            form.save()
            return redirect("forums:show_forum_detail", pk=forum.forums_id)
    else:
        form = ForumsForm(instance=forum)
    return render(
        request, "forums/form.html", {"form": form, "action": "Edit", "forum": forum, "edit_form": True}
    )


@login_required
@require_POST
def forums_delete_view(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    if forum.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this forum.")
    forum.delete()
    return redirect("forums:list")



@login_required
@require_POST
def forum_like_toggle(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    if forum.user_has_liked(request.user):
        forum.forums_likes.remove(request.user)
        liked = False
    else:
        forum.forums_likes.add(request.user)
        liked = True

    return JsonResponse(
        {"forums_likes": forum.forums_likes.count(), "user_has_liked": liked}
    )


@login_required
@require_POST
def reply_like_toggle(request, reply_id):
    reply = get_object_or_404(ForumsReplies, pk=reply_id)
    if reply.user_has_liked(request.user):
        reply.forums_replies_likes.remove(request.user)
        liked = False
    else:
        reply.forums_replies_likes.add(request.user)
        liked = True
    return JsonResponse(
        {"likes": reply.forums_replies_likes.count(), "user_has_liked": liked}
    )



@login_required
@require_POST
def create_reply(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    form = ForumsRepliesForm(request.POST)

    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.forums = forum
        reply.save()

        forum.forums_replies_counts = forum.forum_replies.count()
        forum.save(update_fields=["forums_replies_counts"])

        return JsonResponse(
            {
                "id": reply.id,
                "username": reply.user.username if reply.user else "Anonymous",
                "content": reply.replies_content,
                "created_at": reply.created_at.strftime("%b %d, %Y %H:%M"),
                "likes": reply.forums_replies_likes.count(),
                "is_owner": request.user == reply.user,
                "is_forum_owner": request.user == reply.forums.user,
            }   
        )

    return JsonResponse({"error": "Invalid reply"}, status=400)


@login_required
@require_POST
def load_more_replies(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    offset = int(request.POST.get("offset", 0))
    limit = int(request.POST.get("limit", 5))

    replies = forum.forum_replies.order_by("-created_at")[offset:offset+limit]
    data = []

    for r in replies:
        data.append({
            "id": r.id,
            "username": r.user.username if r.user else "Anonymous",
            "content": r.replies_content,
            "created_at": r.created_at.strftime("%b %d, %Y %H:%M"),
            "likes": r.forums_replies_likes.count(),
        })

    return JsonResponse({"replies": data})


@login_required
@require_POST
def delete_reply(request, reply_id):
    reply = get_object_or_404(ForumsReplies, pk=reply_id)
    if reply.user != request.user and reply.forums.user != request.user:
        return HttpResponseForbidden("Not allowed to delete this reply.")

    parent = reply.forums
    reply.delete()

    parent.forums_replies_counts = parent.forum_replies.count()
    parent.save(update_fields=["forums_replies_counts"])

    return JsonResponse({"deleted": True})
