from django.contrib import admin

from .models import Location
from .models import Schedule
from .models import Slot

# Register your models here.
admin.site.register(Location)
admin.site.register(Schedule)
admin.site.register(Slot)
