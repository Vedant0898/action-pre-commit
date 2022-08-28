from django.db import models
from django.contrib.auth.models import User

from Sports.models import Sport, Venue
# Create your models here.

class Location(models.Model):

    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sport} @ {self.venue}'

class Schedule(models.Model):
    DAYS_OF_WEEK = (
        ("0", 'Monday'),
        ("1", 'Tuesday'),
        ("2", 'Wednesday'),
        ("3", 'Thursday'),
        ("4", 'Friday'),
        ("5", 'Saturday'),
        ("6", 'Sunday'),
    )
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    day = models.CharField(max_length=1,choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day','start_time','end_time']

    def __str__(self):
        return f'{self.start_time}-{self.end_time} ({self.day}) ({self.location})'

class Slot(models.Model):

    STATUS_CHOICES = (
        ("1",'Available'),
        ("2",'Booked'),
        ("3",'Maintenance'),
    )

    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    booking = models.ManyToManyField(User,blank=True)
    courts_booked = models.IntegerField(default=0)

    class Meta:
        ordering = ['date','schedule']
    
    def __str__(self):
        return f'{self.date} {self.status} ({self.schedule})'
    