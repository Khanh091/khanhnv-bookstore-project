from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from framework.views import RegisterView, LoginView, logout_view, BookCatalogView, CartView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('catalog/', BookCatalogView.as_view(), name='book_catalog'),
    path('cart/view/', CartView.as_view(), name='cart_view'),
    path('', RedirectView.as_view(url='/catalog/'), name='home'),
]