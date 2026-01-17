from django.shortcuts import render, redirect
from django.views import View
from .models import Book
from cart.models import Cart, CartItem  # Import từ cart app
from django.contrib import messages

class BookCatalogView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'books/catalog.html', {'books': books})

    def post(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login to add to cart.')
            return redirect('login')

        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        customer_id = request.session['customer_id']

        try:
            book = Book.objects.get(id=book_id)
            if book.stock < quantity:
                messages.error(request, 'Not enough stock.')
                return redirect('book_catalog')

            cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

            # Giảm stock
            book.stock -= quantity
            book.save()

            messages.success(request, 'Added to cart.')
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')

        return redirect('book_catalog')