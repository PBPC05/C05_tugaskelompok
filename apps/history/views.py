from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.history.models import Driver, Winner
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.history.driver_forms import DriverForm
from apps.history.winners_forms import WinnerForm
import json

# Create your views here.

# DRIVER HISTORY
def driver_user_page(request):
    drivers = Driver.objects.all().order_by('year', '-points')
    newest_drivers = Driver.objects.filter(image_url__isnull=False).order_by('-id')[:5]
    return render(request, 'driver_page_user_carousel.html', {
        'drivers': drivers,
        'newest_drivers': newest_drivers
    })

@login_required
def driver_admin_page(request):
    # Kalo bukan admin, redirect ke halaman user
    if not request.user.is_superuser:
        return redirect('history:driver_user_page')

    drivers = Driver.objects.all().order_by('year', '-points')
    newest = Driver.objects.order_by('-id').first() # ambil driver terbaru berdasarkan id nyaa
    return render(request, 'driver_page_admin.html', {
        'drivers': drivers,
        'newest': newest
    })

# CREATE (AJAX)
@csrf_exempt
def add_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver = Driver.objects.create(
            driver_name=data.get('driver_name'),
            nationality=data.get('nationality'),
            car=data.get('car'),
            points=data.get('points'),
            podiums=data.get('podiums'),
            year=data.get('year'),
            image_url=data.get('image_url')
        )
        return JsonResponse({'success': True, 'id': driver.id})
    return JsonResponse({'success': False, 'error': 'Invalid method'})

# DELETE (AJAX)
@csrf_exempt
def delete_driver(request, driver_id):
    if request.method == 'DELETE':
        driver = get_object_or_404(Driver, id=driver_id)
        driver.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid method'})

# EDIT (AJAX)
@csrf_exempt
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        form = DriverForm(data, instance=driver)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid method'})


# WINNER HISTORY
def winner_user_page(request):
    winners = Winner.objects.all().order_by('date')
    newest_winners = Winner.objects.filter(image_url__isnull=False).order_by('-id')[:5]
    return render(request, 'winner_page_user_carousel.html', {
        'winners': winners,
        'newest_winners': newest_winners
    })

@login_required
def winner_admin_page(request):
    # Kalo bukan admin, redirect ke halaman user
    if not request.user.is_superuser:
        return redirect('history:winner_user_page')
    
    winners = Winner.objects.all().order_by('date')
    newest = Winner.objects.order_by('-id').first()  # ambil yang terbaru
    return render(request, 'winner_page_admin.html', {
        'winners': winners,
        'newest': newest
    })


# CREATE (AJAX)
@csrf_exempt
def add_winner(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            winner = Winner.objects.create(
                grand_prix=data.get('grand_prix'),
                date=data.get('date'),
                winner=data.get('winner'),
                car=data.get('car'),
                laps=data.get('laps') or None,
                time=data.get('time'),
                image_url=data.get('image_url') or None
            )

            return JsonResponse({'success': True, 'id': winner.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# DELETE (AJAX)
@csrf_exempt
def delete_winner(request, winner_id):
    if request.method == 'DELETE':
        winner = get_object_or_404(Winner, id=winner_id)
        winner.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid method'})


# EDIT (AJAX)
@csrf_exempt
def edit_winner(request, winner_id):
    winner = get_object_or_404(Winner, id=winner_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        form = WinnerForm(data, instance=winner)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid method'})
