from django.db import models

# Không cần import Customer hay Book nữa

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)  # Dùng string 'app_name.ModelName'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f"Cart for {self.customer.name}"

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.RESTRICT)  # Dùng string 'app_name.ModelName'
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cartitem'

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"