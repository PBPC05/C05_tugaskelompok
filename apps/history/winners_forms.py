from django.forms import ModelForm
from .models import Winner

class WinnerForm(ModelForm):
    class Meta:
        model = Winner
        fields = ['grand_prix', 'date', 'winner', 'car', 'laps', 'time', 'name_code', 'image_url']