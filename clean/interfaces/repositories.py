from abc import ABC, abstractmethod
from domain.entities import Customer, Book, Cart, CartItem

class CustomerRepository(ABC):
    @abstractmethod
    def create(self, customer):
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass

class BookRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, book_id):
        pass

    @abstractmethod
    def update_stock(self, book_id, new_stock):
        pass

class CartRepository(ABC):
    @abstractmethod
    def get_or_create_by_customer(self, customer_id):
        pass

    @abstractmethod
    def get_items(self, cart_id):
        pass

class CartItemRepository(ABC):
    @abstractmethod
    def add_or_update(self, cart_id, book_id, quantity):
        pass