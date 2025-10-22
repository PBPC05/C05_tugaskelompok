from django.shortcuts import render, get_object_or_404
from apps.history.models import Driver

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Driver
from apps.history.driver_forms import DriverForm
import json

# Create your views here.
def show_main(request):
    drivers = Driver.objects.all().order_by('year', '-points')
    return render(request, 'driver_page_admin.html', {'drivers': drivers})

# def driver_user_page(request):
#     drivers = Driver.objects.all().order_by('year', '-points')
#     return render(request, 'driver_page_user_carousel.html', {'drivers': drivers})

def driver_user_page(request):
    drivers = Driver.objects.all().order_by('year', '-points')
    newest_drivers = Driver.objects.filter(image_url__isnull=False).order_by('-id')[:5]
    return render(request, 'driver_page_user_carousel.html', {
        'drivers': drivers,
        'newest_drivers': newest_drivers
    })


# def driver_admin_page(request):
#     drivers = Driver.objects.all().order_by('year', '-points')
#     return render(request, 'driver_page_admin.html', {'drivers': drivers})

def driver_admin_page(request):
    drivers = Driver.objects.all().order_by('year', '-points')
    newest = Driver.objects.order_by('-id').first()  # ambil driver terbaru berdasarkan id nyaa
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