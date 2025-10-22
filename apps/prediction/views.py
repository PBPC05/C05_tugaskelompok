from django.shortcuts import render, get_object_or_404, redirect
from apps.prediction.models import PredictionVote
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

# Create your views here.
def show_main(request):

    return render(request, "prediction_main.html")

def get_votes_json(request):
    try:
        votes_list = PredictionVote.objects.all()
        data = [
            {
                'type': vote.type,
                'race': vote.race,
                'content': vote.content
            }
            for vote in votes_list
        ]

        return JsonResponse(data, safe=False)
    except:
        print("Error")

@require_POST
def post_vote(request):
    type = request.POST.get("type")
    race = request.POST.get("race")
    content = request.POST.get("type")

    vote = PredictionVote(
        type = type,
        race = race,
        content = content,
    )
    vote.save()

    response = redirect('prediction_main.html')
    return response
