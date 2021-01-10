from django.db import models
from accounts.models import User
import string, random

PAYMENT_OPTIONS = (
    ("Mpesa", "MPESA"),
    ("Paypal", "PAYPAL"),
    ("Voucher", "VOUCHER"),
)
CURRENCIES = (
    ("KES", "KES"),
    ("USD", "USD"),
)
PAYMENT_STATUSES = (
    ("Awaiting Payment", "Awaiting Payment"),
    ("Payment Recieved", "Payment Received"),
    ("Payment Updated", "Payment Updated:"),
    ("Completed", "Completed"),
    ("Partially Refunded", "Refunded (Partially)"),
    ("Refunded", "Refunded"),
    ("Failed", "Failed"),
    ("Cancelled", "Cancelled"),
    ("Expired", "Expired"),
)


class Order(models.Model):
    order_id = models.CharField(
        max_length=100,
        primary_key=True,
        unique=True,
        blank=True,
        editable=False,
        null=False,
    )
    user_id = models.ForeignKey(
        "accounts.User", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    total_amount = models.CharField(max_length=30, blank=False, null=False)
    currency = models.CharField(max_length=20, choices=CURRENCIES)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUSES, default="A"
    )

    order_items = models.TextField("items", null=True, default='[]')

    @property
    def billing(self):
        return BillingInfo.objects.filter(order_id=self.order_id).first()

    @property
    def shipping(self):
        return ShippingInfo.objects.filter(order_id=self.order_id).first()

    @classmethod
    def generateId(cls):
        length = 8
        letters = string.ascii_uppercase + string.digits
        result_str = "".join(random.choices(letters, k=6))
        while cls.objects.filter(pk=result_str).exists():
            result_str = "".join(random.choices(letters, k=6))
        return "OR" + result_str

    def save(self, *args, **kwargs):
        if not self.pk or self.pk == "":
            self.pk = self.generateId()
        super().save(*args, **kwargs)


class OrderPayment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    ref = models.CharField(max_length=50, null=True)
    amount = models.CharField(max_length=20, default=0)
    currency = models.CharField(max_length=20, choices=CURRENCIES)
    method = models.CharField(max_length=30, choices=PAYMENT_OPTIONS, null=False)
    date = models.DateTimeField(auto_now_add=True)


class BillingInfo(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, primary_key=True, unique=True
    )
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False)
    phone2 = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(blank=False, null=False)

    state = models.CharField(max_length=50, null=True, blank=False)
    city = models.CharField(max_length=50, null=True, blank=False)
    postal_code = models.CharField(max_length=30, null=True, blank=False)
    country = models.CharField(max_length=32, null=True, blank=False)


class ShippingInfo(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, primary_key=True, unique=True
    )
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False)
    phone2 = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(blank=False, null=False)

    state = models.CharField(max_length=50, null=True, blank=False)
    city = models.CharField(max_length=50, null=True, blank=False)
    postal_code = models.CharField(max_length=30, null=True, blank=False)
    country = models.CharField(max_length=32, null=True, blank=False)
