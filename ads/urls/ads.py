from django.urls import path

from ads.views import ad


urlpatterns = [
    path('', ad.AdListView.as_view(), name="all ads"),
    path('data/', ad.AdDataView.as_view(), name="ads_status"),
    path('<int:pk>/', ad.AdDetailView.as_view(), name="ad"),
    path('create/', ad.AdCreateView.as_view(), name="create ads"),
    path('<int:pk>/update', ad.AdUpdateView.as_view(), name="update ads"),
    path('<int:pk>/upload_image', ad.AdImageView.as_view(), name="upload images for ads"),
    path('<int:pk>/delete', ad.AdDeleteView.as_view(), name="delete ads")
]