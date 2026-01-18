from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
import requests

# API endpoints for microservices
CUSTOMER_SERVICE_URL = 'http://127.0.0.1:8001'
BOOK_SERVICE_URL = 'http://127.0.0.1:8002'
CART_SERVICE_URL = 'http://127.0.0.1:8003'

class RegisterView(View):
    def get(self, request):
        return render(request, 'gateway/register.html')
    
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            response = requests.post(
                f'{CUSTOMER_SERVICE_URL}/api/customers/register/',
                json={'name': name, 'email': email, 'password': password}
            )
            
            if response.status_code == 201:
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')
            else:
                data = response.json()
                messages.error(request, data.get('error', 'Registration failed'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return render(request, 'gateway/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'gateway/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            response = requests.post(
                f'{CUSTOMER_SERVICE_URL}/api/customers/login/',
                json={'email': email, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                request.session['customer_id'] = data['id']
                request.session['customer_name'] = data['name']
                messages.success(request, f'Welcome, {data["name"]}!')
                return redirect('catalog')
            else:
                data = response.json()
                messages.error(request, data.get('error', 'Invalid credentials'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return render(request, 'gateway/login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('login')

class CatalogView(View):
    def get(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login first')
            return redirect('login')
        
        try:
            response = requests.get(f'{BOOK_SERVICE_URL}/api/books/')
            if response.status_code == 200:
                data = response.json()
                books = data.get('books', [])
            else:
                books = []
                messages.error(request, 'Failed to load books')
        except Exception as e:
            books = []
            messages.error(request, f'Error: {str(e)}')
        
        return render(request, 'gateway/catalog.html', {'books': books})
    
    def post(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login first')
            return redirect('login')
        
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        customer_id = request.session['customer_id']
        
        try:
            response = requests.post(
                f'{CART_SERVICE_URL}/api/carts/add/',
                json={
                    'customer_id': customer_id,
                    'book_id': book_id,
                    'quantity': quantity
                }
            )
            
            if response.status_code == 200:
                messages.success(request, 'Book added to cart!')
            else:
                data = response.json()
                messages.error(request, data.get('error', 'Failed to add to cart'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return redirect('catalog')

class CartView(View):
    def get(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login first')
            return redirect('login')
        
        customer_id = request.session['customer_id']
        
        try:
            # Get cart items
            cart_response = requests.get(f'{CART_SERVICE_URL}/api/carts/{customer_id}/')
            
            if cart_response.status_code == 200:
                cart_data = cart_response.json()
                cart_items = cart_data.get('items', [])
                
                # Get book details for each item
                books_response = requests.get(f'{BOOK_SERVICE_URL}/api/books/')
                books_data = {}
                if books_response.status_code == 200:
                    all_books = books_response.json().get('books', [])
                    books_data = {book['id']: book for book in all_books}
                
                # Enrich cart items with book details
                enriched_items = []
                total = 0
                for item in cart_items:
                    book_id = item['book_id']
                    if book_id in books_data:
                        book = books_data[book_id]
                        quantity = item['quantity']
                        price = float(book['price'])
                        enriched_items.append({
                            'book': book,
                            'quantity': quantity,
                            'subtotal': price * quantity
                        })
                        total += price * quantity
                
                return render(request, 'gateway/cart.html', {
                    'items': enriched_items,
                    'total': total
                })
            else:
                messages.error(request, 'Failed to load cart')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return render(request, 'gateway/cart.html', {'items': [], 'total': 0})
