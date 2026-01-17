from django.urls import path
from .views import CartView

urlpatterns = [
    path('view/', CartView.as_view(), name='cart_view'),
]