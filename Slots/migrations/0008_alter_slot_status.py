# Generated by Django 4.1 on 2022-08-29 02:15
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("Slots", "0007_alter_schedule_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slot",
            name="status",
            field=models.CharField(
                choices=[
                    ("1", "Available"),
                    ("2", "Booked"),
                    ("3", "Maintenance"),
                    ("4", "Holiday"),
                ],
                max_length=1,
            ),
        ),
    ]
