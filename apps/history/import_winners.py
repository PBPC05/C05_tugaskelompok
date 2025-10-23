import csv
from apps.history.models import Winner
from datetime import datetime

# Buka file CSV nya
with open('apps/history/csv/winners.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    count = 0
    for i, row in enumerate(reader):
        if i >= 150:  # cuman ngambil 150 data pertama aja
            break

        # Bersihin dan handle nilai yg kosong
        grand_prix = row['Grand Prix'].strip()
        date_str = row['Date'].strip()
        winner_name = row['Winner'].strip()
        car = row['Car'].strip() if row['Car'] else ''
        laps = float(row['Laps']) if row['Laps'].strip() else 0.0
        time = row['Time'].strip() if row['Time'] else '-'
        name_code = row['Name Code'].strip() if row['Name Code'] else None

        # Parse tanggal nya (YYYY-MM-DD)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Format tanggal tidak valid di baris {i+2}: {date_str}")
            continue

        Winner.objects.create(
            grand_prix=grand_prix,
            date=date,
            winner=winner_name,
            car=car,
            laps=laps,
            time=time,
            name_code=name_code,
            image_url=None
        )

        count += 1

print(f"Berhasil import {count} data pertama dari winners.csv!")