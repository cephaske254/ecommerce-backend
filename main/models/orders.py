from django.db import models
from . import User
import string, random


class Order(models.Model):
    order_id = models.CharField(
        max_length=100, primary_key=True, unique=True, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, editable=False
    )
    shipping_name = models.CharField(max_length=255)
    shipping_email = models.EmailField(null=True, blank=True)
    shipping_phone = models.CharField(max_length=20, blank=False, null=False)
    shipping_address1 = models.CharField(max_length=100, blank=False, null=False)
    shipping_address2 = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=70)
    shipping_city = models.CharField(max_length=70)
    shipping_postal_code = models.CharField(max_length=30)

    shipping_cost = models.FloatField(default=0)
    tax = models.FloatField(default=0)

    order_items_json = models.TextField(blank=True, null=False)

    shipping_status = models.CharField(
        choices=(
            ("F", "Firmed"),
            ("R", "Released"),
            ("H", "On Hold"),
            ("S", "Shipped"),
            ("C", "Canceled"),
        ),
        max_length=20,
    )

    payment_method = models.CharField(
        max_length=50,
        null=False,
    )

    amount = models.FloatField(default=0, null=True, editable=False)
    amount_paid = models.FloatField(default=0, null=True, editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.id = self.generate_order_id()
        super().save(*args, **kwargs)

    @classmethod
    def generate_order_id(cls):
        random_order_id = "OR_".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )

        while cls.objects.filter(order_id=random_order_id).exists():
            random_order_id = "OR_".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        return random_order_id
