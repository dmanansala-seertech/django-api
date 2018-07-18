from django.urls import include, path,re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserView, UserDetailsView, \
    FlightCreateView, FlightDetailsView, UserFlightCreateView, UserFlightDetailsView, \
    CarrierCreateView, CarrierDetailsView


urlpatterns = {
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', UserView.as_view(), name="users"),
    path('flights/', FlightCreateView.as_view(), name="flight_create"),
    path('flights/<int:pk>/',FlightDetailsView.as_view(), name="flight_details"),
    path('carriers/', CarrierCreateView.as_view(), name="carrier_create"),
    path('carriers/<int:pk>/',CarrierDetailsView.as_view(), name="carrier_details"),
    path('user_flights/', UserFlightCreateView.as_view(), name="flight_booking_create"),
    path('user_flights/<int:pk>/',UserFlightDetailsView.as_view(), name="flight_booking_details"),
    path('users/<int:pk>/', UserDetailsView.as_view(), name="user_details"),
    path('get-token/', obtain_auth_token), # Add this line
}

urlpatterns = format_suffix_patterns(urlpatterns)
