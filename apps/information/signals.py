from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from .models import Driver, Team
from .csvio import (
    import_circuits_csv, import_races_csv, import_teams_csv,
    import_drivers_csv, import_raceresult_csv
)

def load_seed_once(sender, **kwargs):
    try:   
        if Driver.objects.exists() or Team.objects.exists():
            return
    except (OperationalError, ProgrammingError):
        return

    import_circuits_csv()
    import_races_csv()
    import_teams_csv()
    import_drivers_csv()
    import_raceresult_csv()
