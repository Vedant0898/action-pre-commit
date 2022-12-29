from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Notification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.text[:30]}... @ {self.user}"
