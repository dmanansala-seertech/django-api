from rest_framework import serializers
from .models import Flight, UserFlightlist, Carrier
from django.contrib.auth.models import User
from django.db.models import Q

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FlightSerializer(serializers.ModelSerializer):
    """Serializer to map the model instance into json format."""

    class Meta:
        """Map this serializer to a model and their fields."""
        model = Flight
        fields = ('id', 'name', 'carrier', 'source', 'destination', 'booking_date_from', 'booking_date_to', 'date_created', 'date_modified') # ADD 'owner'
        
        read_only_fields = ('name', 'date_created', 'date_modified')

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if not data['booking_date_from']:
            raise serializers.ValidationError("booking_date_from is required")

        if not data['booking_date_to']:
            raise serializers.ValidationError("booking_date_to is required")

        if data['booking_date_from'] > data['booking_date_to']:
            raise serializers.ValidationError("booking_date_to must occur after booking_date_from")
        return data

class CarrierSerializer(serializers.ModelSerializer):

    class Meta:
        """Map this serializer to a model and their fields."""
        model = Carrier
        fields = ('id', 'carrier_name', 'code', 'date_created', 'date_modified') # ADD 'owner'
        
        read_only_fields = ('date_created', 'date_modified')

    def validate_carrier_name(self, value):
        if not value or str(value).strip() == '':
            raise serializers.ValidationError("name is required")

        return value

    def validate_code(self, value):
        if not value or str(value).strip() == '':
            raise serializers.ValidationError("code is required")

        return value


class UserFlightlistSerializer(serializers.ModelSerializer):
    """Serializer to map the model instance into json format."""

    owner = serializers.ReadOnlyField(source='owner.username') # ADD THIS LINE
    name = serializers.ReadOnlyField(source='flight.name') # ADD THIS LINE
    source = serializers.ReadOnlyField(source='flight.source') # ADD THIS LINE
    destination = serializers.ReadOnlyField(source='flight.destination') # ADD THIS LINE
    booking_date_from = serializers.ReadOnlyField(source='flight.booking_date_from') # ADD THIS LINE
    booking_date_to = serializers.ReadOnlyField(source='flight.booking_date_to') # ADD THIS LINE

    class Meta:
        """Map this serializer to a model and their fields."""
        model = UserFlightlist
        fields = ('id', 'flight', 'name', 'source', 'destination', 'booking_date_from', 'booking_date_to', 'owner', 'date_created', 'date_modified') # ADD 'owner'
        read_only_fields = ('date_created', 'date_modified')

    def validate_flight(self, value):
        """
        Check that this booking does not conflict with selected bookings
        """
        user = self.context.get("request").user
        if UserFlightlist.objects.filter(flight__id=value.id,owner=user).count() > 0:
            raise serializers.ValidationError("Flight already booked")

        selected_flight = Flight.objects.filter(id=value.id)[0]
    
        if UserFlightlist.objects.filter(~Q(Q(flight__booking_date_from__gte = selected_flight.booking_date_to) | Q(flight__booking_date_to__lte = selected_flight.booking_date_from)),
            flight__booking_date_from__gt=selected_flight.booking_date_from, owner=user).count() > 0:
            logger.error("Event conflicts with your other existing flights 1")

            raise serializers.ValidationError("Event conflicts with your other existing flights")

        if UserFlightlist.objects.filter(~Q(Q(flight__booking_date_to__lte = selected_flight.booking_date_from) | Q(flight__booking_date_from__gte = selected_flight.booking_date_to)),
            flight__booking_date_from__lt = selected_flight.booking_date_from, owner=user).count() > 0:
            logger.error("Event conflicts with your other existing flights 2")
            raise serializers.ValidationError("Event conflicts with your other existing flights")

        return value



class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username')
