from django.contrib import admin

from .models import Order, OrderProduct, ShippingAddress, City

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(City)
