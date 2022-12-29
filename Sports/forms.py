from django import forms

from .models import Inventory
from .models import Sport
from .models import Venue


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        exclude = ()


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        exclude = ("sport",)


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        exclude = ("sport",)
