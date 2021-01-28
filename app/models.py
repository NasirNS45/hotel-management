from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin


class RoomBooking(models.Model):
    checkin = models.CharField(max_length=140, default='NULL')
    checkout = models.CharField(max_length=140, default='NULL')
    firstname = models.CharField(max_length=140)
    middlename = models.CharField(max_length=140)
    lastname = models.CharField(max_length=140)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.TextField(max_length=400)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)
    zipcode = models.IntegerField()
    idproof = models.CharField(max_length=140)
    rooms = models.CharField(max_length=40)

    def __str__(self):
        return '{} {}'.format(self.checkin, self.checkout)


class BookingHistory(models.Model):
    checkin = models.CharField(max_length=140, default='NULL')
    checkout = models.CharField(max_length=140, default='NULL')
    email = models.EmailField(max_length=50)
    userid = models.BigIntegerField(default=0)
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.checkin, self.checkout)


class Rooms(models.Model):
    roomtype = models.CharField(max_length=140, default='NULL')
    total = models.BigIntegerField(default=0)
    available = models.BigIntegerField(default=0)

    def __str__(self):
        return '{} {} {}'.format(self.roomtype, self.total, self.available)
