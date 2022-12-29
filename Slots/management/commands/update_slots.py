from datetime import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from Slots.models import Schedule
from Slots.models import Slot


class Command(BaseCommand):
    help = "add slot for all location according to given schedule"

    def handle(self, *args, **options):
        for i in range(8):
            dt = datetime.now() + timedelta(days=i)
            day = dt.weekday()
            sched = Schedule.objects.filter(day=day)
            cnt = 0
            for sch in sched:
                loc = sch.location
                if not Slot.objects.filter(
                    location=loc, schedule=sch, date=dt
                ).exists():
                    Slot.objects.create(location=loc, schedule=sch, date=dt, status="1")
                    cnt += 1

            self.stdout.write(f"Successfully added {cnt} slots on {dt}.")
