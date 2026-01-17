from django.shortcuts import render, redirect
from django.views import View
from django import forms
from .models import Customer
from django.contrib import messages

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'password']

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                customer = Customer.objects.get(email=email, password=password)
                request.session['customer_id'] = customer.id
                return redirect('/books/catalog/')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')