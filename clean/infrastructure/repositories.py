from interfaces.repositories import CustomerRepository, BookRepository, CartRepository, CartItemRepository
from domain.entities import Customer, Book, Cart, CartItem
from .models import CustomerModel, BookModel, CartModel, CartItemModel
from django.core.exceptions import ObjectDoesNotExist

class CustomerRepositoryImpl(CustomerRepository):
    def create(self, customer):
        model = CustomerModel(name=customer.name, email=customer.email, password=customer.password)
        model.save()
        customer.id = model.id
        return customer

    def get_by_email(self, email):
        try:
            model = CustomerModel.objects.get(email=email)
            return Customer(id=model.id, name=model.name, email=model.email, password=model.password)
        except ObjectDoesNotExist:
            return None

class BookRepositoryImpl(BookRepository):
    def get_all(self):
        models = BookModel.objects.all()
        return [Book(id=m.id, title=m.title, author=m.author, price=m.price, stock=m.stock) for m in models]

    def get_by_id(self, book_id):
        try:
            m = BookModel.objects.get(id=book_id)
            return Book(id=m.id, title=m.title, author=m.author, price=m.price, stock=m.stock)
        except ObjectDoesNotExist:
            return None

    def update_stock(self, book_id, new_stock):
        BookModel.objects.filter(id=book_id).update(stock=new_stock)

class CartRepositoryImpl(CartRepository):
    def get_or_create_by_customer(self, customer_id):
        model, _ = CartModel.objects.get_or_create(customer_id=customer_id)
        return Cart(id=model.id, customer_id=customer_id, created_at=model.created_at)

    def get_items(self, cart_id):
        models = CartItemModel.objects.filter(cart_id=cart_id)
        return [CartItem(id=m.id, cart_id=m.cart_id, book_id=m.book.id, quantity=m.quantity) for m in models]

class CartItemRepositoryImpl(CartItemRepository):
    def add_or_update(self, cart_id, book_id, quantity):
        item, created = CartItemModel.objects.get_or_create(cart_id=cart_id, book_id=book_id)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()