from django.forms import ModelForm
from .models import Driver

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['driver_name', 'nationality', 'car', 'points', 'podiums', 'year', 'image_url']