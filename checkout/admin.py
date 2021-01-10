from django.contrib import admin
from .models import Order, OrderPayment, BillingInfo, ShippingInfo

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderPayment)
admin.site.register(ShippingInfo)
admin.site.register(BillingInfo)
