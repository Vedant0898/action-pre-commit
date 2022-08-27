from django.contrib import admin

from .models import Location, Schedule, Slot
# Register your models here.
admin.site.register(Location)
admin.site.register(Schedule)
admin.site.register(Slot)