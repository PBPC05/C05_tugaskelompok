from django.shortcuts import render
from apps.history.models import Driver

# Create your views here.
def show_main(request):
    drivers = Driver.objects.all().order_by('year', '-points')
    return render(request, 'history_page.html', {'drivers': drivers})

def history_page(request):
    drivers = Driver.objects.all().order_by('year', '-points')
    return render(request, 'history_page.html', {'drivers': drivers})