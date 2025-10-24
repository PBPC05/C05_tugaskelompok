from django.contrib import admin
from apps.history.models import Driver, Winner

# Register your models here.
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_name', 'nationality', 'car', 'points', 'year')
    search_fields = ('driver_name', 'nationality', 'car')

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('grand_prix', 'winner', 'car', 'date', 'laps', 'time')
    search_fields = ('winner', 'grand_prix', 'car')