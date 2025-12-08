from django.shortcuts import render, get_object_or_404, redirect
from apps.prediction.models import PredictionVote
from apps.information.models import Race
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def show_main(request):
    context = {
        'user_has_voted': request.session.get('user_has_voted')
    }
    return render(request, "prediction_main.html", context)

def get_votes_json(request):
    data = list(PredictionVote.objects.values("vote_type", "race", "content"))
    return JsonResponse(data, safe=False)

@require_POST
@login_required
def post_vote(request):
    try:
        user = request.user
        vote_type = request.POST.get("vote_type")
        race = request.POST.get("race")
        content = request.POST.get("content")

        vote = PredictionVote(
            user = user,
            vote_type = vote_type,
            race = race,
            content = content,
        )
        vote.save()

        request.session['user_has_voted'] = True
        request.session.save()

        return JsonResponse({"success": True})
    except Exception as e:
        print(e)

@require_POST
@login_required
@user_passes_test(lambda u: u.is_superuser)
def clear_votes(request):
    PredictionVote.objects.all().delete()
    return JsonResponse({"success": True})

#
# Flutter related views
#

@csrf_exempt
def post_vote_flutter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        vote_type = data.get("vote_type", "")
        race = data.get("race", "")
        content = data.get("content", "")

        new_vote = PredictionVote(
            user = user,
            vote_type = vote_type,
            race = race,
            content = content
        )
        new_vote.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)