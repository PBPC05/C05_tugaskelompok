from django.shortcuts import render, get_object_or_404, redirect
from apps.prediction.models import PredictionVote
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core import serializers
from django.contrib.auth.decorators import login_required
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
