from django import forms

from .models import Location, Schedule

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        exclude = ()


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        exclude = ()
