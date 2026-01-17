from django.urls import path
from .views import BookCatalogView

urlpatterns = [
    path('catalog/', BookCatalogView.as_view(), name='book_catalog'),
]