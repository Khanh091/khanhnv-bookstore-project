from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Customer
import json

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Register a new customer"""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        customer = Customer.objects.create(name=name, email=email, password=password)
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Login customer"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return JsonResponse({'error': 'Missing email or password'}, status=400)
        
        try:
            customer = Customer.objects.get(email=email, password=password)
            return JsonResponse({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email
            }, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_customer(request, customer_id):
    """Get customer by ID"""
    try:
        customer = Customer.objects.get(id=customer_id)
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
