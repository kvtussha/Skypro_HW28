from django.contrib import admin
from django.urls import path, include

from ads.views.start_view import status_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', status_view, name="status view"),

    path('cat/', include('ads.urls.categories'), name="categories"),
    path('ad/', include('ads.urls.ads'), name="ads"),
    path('loc/', include('ads.urls.locations'), name="locations"),
    path('user/', include('ads.urls.users'), name="users")
]
