from domain.entities import Customer, CartItem
from django.contrib import messages

class RegisterCustomerUseCase:
    def __init__(self, customer_repo):
        self.customer_repo = customer_repo

    def execute(self, name, email, password):
        if self.customer_repo.get_by_email(email):
            return None  # Already exists
        customer = Customer(name=name, email=email, password=password)
        return self.customer_repo.create(customer)

class LoginCustomerUseCase:
    def __init__(self, customer_repo):
        self.customer_repo = customer_repo

    def execute(self, email, password):
        customer = self.customer_repo.get_by_email(email)
        if customer and customer.password == password:
            return customer
        return None

class GetBookCatalogUseCase:
    def __init__(self, book_repo):
        self.book_repo = book_repo

    def execute(self):
        return self.book_repo.get_all()

class AddToCartUseCase:
    def __init__(self, book_repo, cart_repo, cart_item_repo):
        self.book_repo = book_repo
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo

    def execute(self, customer_id, book_id, quantity, request):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            messages.error(request, 'Book not found.')
            return False
        if book.stock < quantity:
            messages.error(request, 'Not enough stock.')
            return False
        cart = self.cart_repo.get_or_create_by_customer(customer_id)
        self.cart_item_repo.add_or_update(cart.id, book_id, quantity)
        self.book_repo.update_stock(book_id, book.stock - quantity)
        messages.success(request, 'Added to cart.')
        return True

class GetCartContentsUseCase:
    def __init__(self, cart_repo, book_repo):
        self.cart_repo = cart_repo
        self.book_repo = book_repo

    def execute(self, customer_id):
        cart = self.cart_repo.get_or_create_by_customer(customer_id)
        items = self.cart_repo.get_items(cart.id)
        enriched_items = []
        total = 0
        for item in items:
            book = self.book_repo.get_by_id(item.book_id)
            if book:
                enriched_items.append({'book': book, 'quantity': item.quantity})
                total += book.price * item.quantity
        return {'items': enriched_items, 'total': total}