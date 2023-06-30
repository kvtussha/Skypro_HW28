from django.urls import path

from ads.views import location


urlpatterns = [
    path('data/', location.LocationDataView.as_view(), name="location data")
]