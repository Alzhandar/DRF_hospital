from django.utils import timezone
from api.models import Visit
import datetime

def get_upcoming_visits_count():
    return Visit.objects.filter(schedule__timestamp_start__gte=datetime.datetime.now()).count()
