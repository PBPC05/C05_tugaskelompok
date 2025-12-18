from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

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
        qs = qs.order_by("-is_hot", "-created_at")
    elif filter_type == "oldest":
        qs = qs.order_by("-is_hot", "created_at")
    elif filter_type == "hot":
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        qs = qs.filter(created_at__gte=one_week_ago).order_by("-is_hot", "-forums_views")
    elif filter_type == "popular":
        qs = qs.order_by("-is_hot", "-forums_views")

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
            "is_hot": f.is_hot,
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
    if forum.user != request.user and not request.user.is_staff:
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

    user_has_liked = (
        forum.user_has_liked(request.user)
        if request.user.is_authenticated
        else False
    )

    for r in replies:
        if request.user.is_authenticated:
            user_has_liked = r.user_has_liked(request.user)
        else:
            r.user_has_liked = False
        data.append({
            "id": r.id,
            "username": r.user.username if r.user else "Anonymous",
            "content": r.replies_content,
            "created_at": r.created_at.strftime("%b %d, %Y %H:%M"),
            "likes": r.forums_replies_likes.count(),
            "is_owner": request.user == r.user,
            "is_forum_owner": request.user == r.forums.user,
            "user_has_liked": user_has_liked,
            'is_admin': request.user.is_staff,
        })

    return JsonResponse({"replies": data})


@login_required
@require_POST
def delete_reply(request, reply_id):
    reply = get_object_or_404(ForumsReplies, pk=reply_id)
    if reply.user != request.user and reply.forums.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed to delete this reply.")

    parent = reply.forums
    reply.delete()

    parent.forums_replies_counts = parent.forum_replies.count()
    parent.save(update_fields=["forums_replies_counts"])

    return JsonResponse({"deleted": True})

@staff_member_required
def toggle_hot_forum(request, pk):
    forum = get_object_or_404(Forums, forums_id=pk)
    forum.is_hot = not forum.is_hot
    forum.save(update_fields=["is_hot"])
    return JsonResponse({"is_hot": forum.is_hot})




# Get all replies for a forum
def forum_replies_json(request, pk):
    try:
        forum = get_object_or_404(Forums, forums_id=pk)
        replies = forum.forum_replies.order_by("-created_at").all()
        
        data = []
        for reply in replies:
            data.append({
                "id": reply.id,
                "username": reply.user.username if reply.user else "Anonymous",
                "content": reply.replies_content,
                "likes": reply.forums_replies_likes.count(),
                "created_at": reply.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                "user_has_liked": reply.user_has_liked(request.user) if request.user.is_authenticated else False,
                "is_owner": request.user == reply.user,
                "is_forum_owner": request.user == forum.user,
            })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Create a reply
def create_reply_flutter(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        forum = get_object_or_404(Forums, forums_id=pk)
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({"status": "error", "message": "Content required"}, status=400)
        
        reply = ForumsReplies.objects.create(
            forums=forum,
            user=request.user,
            replies_content=content
        )
        
        forum.forums_replies_counts = forum.forum_replies.count()
        forum.save(update_fields=["forums_replies_counts"])
        
        return JsonResponse({
            "status": "success",
            "id": reply.id,
            "username": reply.user.username,
            "content": reply.replies_content,
            "likes": 0,
            "created_at": reply.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "user_has_liked": False,
            "is_owner": True,
            "is_forum_owner": request.user == forum.user,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Delete a reply
def delete_reply_flutter(request, reply_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        reply = get_object_or_404(ForumsReplies, id=reply_id)
        
        # Check permissions
        if not (request.user == reply.user or request.user == reply.forums.user or request.user.is_staff):
            return JsonResponse({"status": "error", "message": "Permission denied"}, status=403)
        
        forum = reply.forums
        reply.delete()
        
        forum.forums_replies_counts = forum.forum_replies.count()
        forum.save(update_fields=["forums_replies_counts"])
        
        return JsonResponse({"status": "success", "message": "Reply deleted"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Toggle reply like
def toggle_reply_like_flutter(request, reply_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        reply = get_object_or_404(ForumsReplies, id=reply_id)
        
        if reply.user_has_liked(request.user):
            reply.forums_replies_likes.remove(request.user)
            liked = False
        else:
            reply.forums_replies_likes.add(request.user)
            liked = True
        
        return JsonResponse({
            "status": "success",
            "likes": reply.forums_replies_likes.count(),
            "user_has_liked": liked
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Create forum (Flutter version)
def create_forum_flutter(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title or not content:
            return JsonResponse({"status": "error", "message": "Title and content required"}, status=400)
        
        forum = Forums.objects.create(
            user=request.user,
            title=title,
            content=content
        )
        
        return JsonResponse({
            "status": "success",
            "forums_id": str(forum.forums_id),
            "title": forum.title,
            "content": forum.content,
            "username": request.user.username,
            "forums_views": 0,
            "forums_likes": 0,
            "forums_replies_counts": 0,
            "is_hot": False,
            "created_at": forum.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "user_has_liked": False,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Update forum (Flutter version)
def update_forum_flutter(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        forum = get_object_or_404(Forums, forums_id=pk)
        
        # Check ownership
        if forum.user != request.user and not request.user.is_staff:
            return JsonResponse({"status": "error", "message": "Permission denied"}, status=403)
        
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title or not content:
            return JsonResponse({"status": "error", "message": "Title and content required"}, status=400)
        
        forum.title = title
        forum.content = content
        forum.save()
        
        return JsonResponse({
            "status": "success",
            "forums_id": str(forum.forums_id),
            "title": forum.title,
            "content": forum.content,
            "username": forum.user.username,
            "forums_views": forum.forums_views,
            "forums_likes": forum.forums_likes.count(),
            "forums_replies_counts": forum.forums_replies_counts,
            "is_hot": forum.is_hot,
            "created_at": forum.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "user_has_liked": forum.user_has_liked(request.user),
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Delete forum (Flutter version)
def delete_forum_flutter(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        forum = get_object_or_404(Forums, forums_id=pk)
        
        # Check ownership
        if forum.user != request.user and not request.user.is_staff:
            return JsonResponse({"status": "error", "message": "Permission denied"}, status=403)
        
        forum.delete()
        return JsonResponse({"status": "success", "message": "Forum deleted"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Toggle forum like (Flutter version)
def toggle_forum_like_flutter(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Login required"}, status=401)
    
    try:
        forum = get_object_or_404(Forums, forums_id=pk)
        
        if forum.user_has_liked(request.user):
            forum.forums_likes.remove(request.user)
            liked = False
        else:
            forum.forums_likes.add(request.user)
            liked = True
        
        return JsonResponse({
            "status": "success",
            "forums_likes": forum.forums_likes.count(),
            "user_has_liked": liked
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Toggle hot status (Flutter version)
def toggle_hot_forum_flutter(request, pk):
    if not request.user.is_staff:
        return JsonResponse({"status": "error", "message": "Admin only"}, status=403)
    
    try:
        forum = get_object_or_404(Forums, forums_id=pk)
        forum.is_hot = not forum.is_hot
        forum.save(update_fields=["is_hot"])
        
        return JsonResponse({
            "status": "success",
            "is_hot": forum.is_hot,
            "message": f"Forum marked as {'hot' if forum.is_hot else 'not hot'}"
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@require_GET
def check_admin(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'is_logged_in': False,
            'is_admin': False,
            'is_staff': False,
            'user_id': None,
            'username': None,
        }, status=200)
    
    user = request.user
    return JsonResponse({
        'is_logged_in': True,
        'is_admin': user.is_superuser or user.is_staff,
        'is_staff': user.is_staff,
        'user_id': user.id,
        'username': user.username,
    })

@require_GET
def get_user_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'is_logged_in': False}, status=200)
    
    user = request.user
    return JsonResponse({
        'is_logged_in': True,
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    })
