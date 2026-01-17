from django.shortcuts import render, redirect
from django.views import View
from .models import Cart
from django.contrib import messages

class CartView(View):
    def get(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login to view cart.')
            return redirect('login')

        customer_id = request.session['customer_id']
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = cart.cartitem_set.all()
            total = sum(item.book.price * item.quantity for item in items)
            return render(request, 'cart/view.html', {'items': items, 'total': total})
        except Cart.DoesNotExist:
            return render(request, 'cart/view.html', {'items': [], 'total': 0})