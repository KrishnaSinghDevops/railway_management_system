from django.db import models

from django.db import models


class Train(models.Model):
    TRAIN_ID = models.AutoField(primary_key=True)
    TRAIN_NUMBER = models.CharField(max_length=20)
    TRAIN_NAME = models.CharField(max_length=200)
    SOURCE_STATION = models.CharField(max_length=100)
    DESTINATION_STATION = models.CharField(max_length=100)
    DEPARTURE_TIME = models.TimeField()
    ARRIVAL_TIME = models.TimeField()
    TOTAL_SEATS = models.IntegerField()
    AVAILABLE_SEATS = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TRAINS'


class Booking(models.Model):
    BOOKING_ID = models.AutoField(primary_key=True)
    PNR_NUMBER = models.CharField(max_length=50)
    USER_ID = models.IntegerField()
    TRAIN_ID = models.IntegerField()
    JOURNEY_DATE = models.DateField()
    PASSENGER_NAME = models.CharField(max_length=200)
    PASSENGER_AGE = models.IntegerField()
    PASSENGER_GENDER = models.CharField(max_length=20)
    SEAT_NUMBER = models.CharField(max_length=20)
    STATUS = models.CharField(max_length=50)
    CREATED_AT = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'BOOKINGS'

