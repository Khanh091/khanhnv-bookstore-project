from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_items', 'total_price', 'created_at')

    def total_items(self, obj):
        return obj.cartitem_set.count()
    total_items.short_description = 'Tổng Item'

    def total_price(self, obj):
        return sum(item.book.price * item.quantity for item in obj.cartitem_set.all())
    total_price.short_description = 'Tổng Giá'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)