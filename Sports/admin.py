from django.contrib import admin

from .models import Inventory
from .models import Sport
from .models import Venue

# Register your models here.
admin.site.register(Sport)
admin.site.register(Venue)
admin.site.register(Inventory)
