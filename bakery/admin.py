from django.contrib import admin
from .models import Cake, Customer, Cart, Order, Wishlist

admin.site.register(Cake)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Wishlist)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'phone',
        'total_amount',
        'payment_method',
        'status',
        'order_date'
    )

    list_filter = (
        'status',
        'payment_method'
    )

    search_fields = (
        'customer_name',
        'phone'
    )