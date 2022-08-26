from django.db import models

# Create your models here.
class Sport(models.Model):

    name = models.CharField(max_length=50,unique=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Sports"

class Inventory(models.Model):

    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,help_text="Name of Equipment")
    quantity = models.IntegerField()


    def __str__(self):
        return f'{self.sport} - {self.name}'
    
    class Meta:
        verbose_name_plural = "Inventory"

class Venue(models.Model):

    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,help_text="Name of Venue eg. Room No., Court No. etc")
    no_of_courts = models.IntegerField(help_text="Number of courts available in this Venue")
    
    def __str__(self):
        return f'{self.sport} - {self.name}'
    
    class Meta:
        verbose_name_plural = "Venues"

