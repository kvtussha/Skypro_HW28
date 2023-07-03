from django.urls import path

from ads.views import category


urlpatterns = [
    path('data/', category.CategoryDataView.as_view(), name="category_list"),
    path('', category.CategoryListView.as_view(), name="all categories"),
    path('<int:pk>/', category.CategoryDetailView.as_view(), name="category"),
    path('create/', category.CategoryCreateView.as_view(), name="create categories"),
    path('<int:pk>/update/', category.CategoryUpdateView.as_view(), name="update categories"),
    path('<int:pk>/delete/', category.CategoryDeleteView.as_view(), name="delete categories")
]