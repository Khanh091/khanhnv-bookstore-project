"""
URL configuration for customer_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from customers import views as customer_views
from gateway import views as gateway_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/customers/register/', customer_views.register, name='api_register'),
    path('api/customers/login/', customer_views.login, name='api_login'),
    path('api/customers/<int:customer_id>/', customer_views.get_customer, name='api_get_customer'),
    # Gateway/frontend endpoints
    path('', gateway_views.CatalogView.as_view(), name='home'),
    path('register/', gateway_views.RegisterView.as_view(), name='register'),
    path('login/', gateway_views.LoginView.as_view(), name='login'),
    path('logout/', gateway_views.logout_view, name='logout'),
    path('catalog/', gateway_views.CatalogView.as_view(), name='catalog'),
    path('cart/', gateway_views.CartView.as_view(), name='cart'),
]
