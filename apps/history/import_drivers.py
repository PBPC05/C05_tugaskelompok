import csv
from apps.history.models import Driver

# Buka file CSV nya
with open('apps/history/csv/drivers_updated.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for i, row in enumerate(reader):
        if i >= 150:  # cuman ngambil 150 data pertama aja
            break
        
        # Buat instance Driver nya
        Driver.objects.create(
            podiums=int(row['Pos']),
            driver_name=row['Driver'].strip(),
            nationality=row['Nationality'],
            car=row['Car'],
            points=float(row['PTS']),
            year=int(row['year']),
            driver_code=row['Code']
        )

print("Berhasil import 150 data pertama dari drivers_updated.csv")