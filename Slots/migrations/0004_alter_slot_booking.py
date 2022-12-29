# Generated by Django 4.1 on 2022-08-27 05:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Slots", "0003_alter_slot_booking"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slot",
            name="booking",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
