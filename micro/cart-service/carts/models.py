from django.db import models

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()  # Reference to customer-service
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['id']

    def __str__(self):
        return f"Cart {self.id} for Customer {self.customer_id}"

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()  # Reference to book-service
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'CartItem'
        ordering = ['id']

    def __str__(self):
        return f"CartItem {self.id}: Book {self.book_id} x{self.quantity}"
