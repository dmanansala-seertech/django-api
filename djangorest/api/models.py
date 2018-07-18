from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Carrier(models.Model):
    carrier_name = models.CharField(max_length=255, blank=False, unique=True)
    code = models.CharField(max_length=16, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.carrier_name)


class Flight(models.Model):
    source = models.CharField(max_length=255, blank=False)
    destination = models.CharField(max_length=255, blank=False)
    booking_date_from = models.DateTimeField('booking date from')
    booking_date_to = models.DateTimeField('booking date to')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    carrier = models.ForeignKey(Carrier, related_name='flights', on_delete=models.CASCADE)

    def name(self):
        return self.carrier.code + "-" + '{:04d}'.format(self.id)
 
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return self.carrier.code + "-" + '{:04d}'.format(self.id)


class UserFlightlist(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='user_flights', on_delete=models.CASCADE) 
    flight = models.ForeignKey(Flight, related_name='linked_flights', on_delete=models.CASCADE)

    def has_schedule_conflict(self):
        return False


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
