from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Book

@require_http_methods(["GET"])
def list_books(request):
    """Get all books catalog"""
    try:
        books = Book.objects.all()
        books_data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'stock': book.stock
        } for book in books]
        return JsonResponse({'books': books_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_book(request, book_id):
    """Get book by ID"""
    try:
        book = Book.objects.get(id=book_id)
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'stock': book.stock
        }, status=200)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
