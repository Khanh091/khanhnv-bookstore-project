from django.shortcuts import render, redirect
from django.views import View
from django import forms
from django.contrib import messages

# Import sau khi path đã đúng
from usecases.usecases import (
    RegisterCustomerUseCase,
    LoginCustomerUseCase,
    GetBookCatalogUseCase,
    AddToCartUseCase,
    GetCartContentsUseCase
)
from infrastructure.repositories import (
    CustomerRepositoryImpl,
    BookRepositoryImpl,
    CartRepositoryImpl,
    CartItemRepositoryImpl
)

# Inject repositories
customer_repo = CustomerRepositoryImpl()
book_repo = BookRepositoryImpl()
cart_repo = CartRepositoryImpl()
cart_item_repo = CartItemRepositoryImpl()

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            usecase = RegisterCustomerUseCase(customer_repo)
            customer = usecase.execute(**form.cleaned_data)
            if customer:
                messages.success(request, 'Registration successful. Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Email already exists.')
        return render(request, 'register.html', {'form': form})

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            usecase = LoginCustomerUseCase(customer_repo)
            customer = usecase.execute(**form.cleaned_data)
            if customer:
                request.session['customer_id'] = customer.id
                return redirect('book_catalog')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

class BookCatalogView(View):
    def get(self, request):
        usecase = GetBookCatalogUseCase(book_repo)
        books = usecase.execute()
        return render(request, 'catalog.html', {'books': books})

    def post(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login to add to cart.')
            return redirect('login')

        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))

        usecase = AddToCartUseCase(book_repo, cart_repo, cart_item_repo)
        usecase.execute(request.session['customer_id'], book_id, quantity, request)
        return redirect('book_catalog')

class CartView(View):
    def get(self, request):
        if 'customer_id' not in request.session:
            messages.error(request, 'Please login to view cart.')
            return redirect('login')

        usecase = GetCartContentsUseCase(cart_repo, book_repo)
        cart_data = usecase.execute(request.session['customer_id'])
        return render(request, 'cart_view.html', {
            'items': cart_data['items'],
            'total': cart_data['total']
        })