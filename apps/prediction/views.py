from django.shortcuts import render, get_object_or_404, redirect
from apps.prediction.models import PredictionVote
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

# Create your views here.
def show_main(request):
    return render(request, "prediction_main.html")

def get_votes_json(request):
    votes_list = PredictionVote.objects.all()
    data = [
        {
            'vote_type': vote.vote_type,
            'race': vote.race,
            'content': vote.content
        }
        for vote in votes_list
    ]

    return JsonResponse(data, safe=False)

@require_POST
def post_vote(request):
    try:
        vote_type = request.POST.get("vote_type")
        race = request.POST.get("race")
        content = request.POST.get("content")

        vote = PredictionVote(
            vote_type = vote_type,
            race = race,
            content = content,
        )
        vote.save()

        return JsonResponse({"success": True})
    except Exception as e:
        print(e)
