from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Cart, CartItem
import json

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    """Add book to cart or update quantity"""
    try:
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        book_id = data.get('book_id')
        quantity = data.get('quantity', 1)
        
        if not all([customer_id, book_id]):
            return JsonResponse({'error': 'Missing customer_id or book_id'}, status=400)
        
        # Get or create cart for customer
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        
        # Get or create cart item
        cart_item, created_item = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        
        if not created_item:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'message': 'Item added to cart',
            'cart_id': cart.id,
            'item_id': cart_item.id,
            'quantity': cart_item.quantity
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_cart(request, customer_id):
    """Get cart contents for a customer"""
    try:
        # Get or create cart for customer
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        
        # Get all cart items
        cart_items = CartItem.objects.filter(cart=cart)
        
        items_data = [{
            'id': item.id,
            'book_id': item.book_id,
            'quantity': item.quantity
        } for item in cart_items]
        
        return JsonResponse({
            'cart_id': cart.id,
            'customer_id': customer_id,
            'items': items_data
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
