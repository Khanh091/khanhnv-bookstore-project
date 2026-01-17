from django.db import models
from accounts.models import Customer
from books.models import Book

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f"Cart for {self.customer.name}"

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cartitem'

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"