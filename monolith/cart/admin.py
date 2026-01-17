from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_items', 'total_price', 'created_at')

    def total_items(self, obj):
        return obj.cartitem_set.count()  # Tính tổng số item trong giỏ
    total_items.short_description = 'Tổng Item'  # Tên cột trong admin (tùy chọn)

    def total_price(self, obj):
        return sum(item.book.price * item.quantity for item in obj.cartitem_set.all())  # Tính tổng giá
    total_price.short_description = 'Tổng Giá'  # Tên cột trong admin (tùy chọn)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)