class Customer:
    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

class Book:
    def __init__(self, id=None, title=None, author=None, price=None, stock=0):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

class Cart:
    def __init__(self, id=None, customer_id=None, created_at=None):
        self.id = id
        self.customer_id = customer_id
        self.created_at = created_at

class CartItem:
    def __init__(self, id=None, cart_id=None, book_id=None, quantity=1):
        self.id = id
        self.cart_id = cart_id
        self.book_id = book_id
        self.quantity = quantity