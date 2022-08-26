from django.contrib import admin
from .models import Sport, Venue, Inventory

# Register your models here.
admin.site.register(Sport)
admin.site.register(Venue)
admin.site.register(Inventory)