from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import UserSerializer, CarrierSerializer, FlightSerializer, UserFlightlistSerializer
from .models import Flight, UserFlightlist, Carrier
from django.contrib.auth.models import User


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Create your views here.
class FlightCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Flight.objects.all()
        carrier = self.request.query_params.get('carrier', None)
        if carrier is not None:
            queryset = queryset.filter(carrier__id=carrier)
            
        source = self.request.query_params.get('source', None)
        if source is not None:
            queryset = queryset.filter(source__icontains=source)
        return queryset
    
    
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        serializer.save()

class FlightDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


# Create your views here.
class CarrierCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer

    def perform_create(self, serializer):
        serializer.save()

class CarrierDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer


# Create your views here.
class UserFlightCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return UserFlightlist.objects.filter(owner=user)
    
    serializer_class = UserFlightlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner) # ADD THIS LINE

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(owner=self.request.user) # Add owner=self.request.user

class UserFlightDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = UserFlightlist.objects.all()
    serializer_class = UserFlightlistSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsOwner)
