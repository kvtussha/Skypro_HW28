from django.urls import path

from ads.views import user


urlpatterns = [
    path('data/', user.UserDataView.as_view(), name="category_list"),
    path('', user.UserListView.as_view(), name="all categories"),
    path('<int:pk>/', user.UserDetailView.as_view(), name="category"),
    path('create/', user.UserCreateView.as_view(), name="create categories"),
    path('<int:pk>/update/', user.UserUpdateView.as_view(), name="update categories"),
    path('<int:pk>/delete/', user.UserDeleteView.as_view(), name="delete categories")
]
