import json
from rest_framework import serializers
from .models import Order, OrderPayment, ShippingInfo, BillingInfo


class ShippingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = "__all__"
        extra_kwargs = {"order": {"read_only": True}}


class BillingInfoSerializer(ShippingInfoSerializer):
    class Meta(ShippingInfoSerializer.Meta):
        model = BillingInfo


class OrderSerializer(serializers.ModelSerializer):
    shipping = ShippingInfoSerializer(required=False)
    billing = BillingInfoSerializer(required=False)
    order_items = serializers.SerializerMethodField("get_items")

    class Meta:
        model = Order
        fields = "__all__"

    def get_items(self, obj):
        items = obj.order_items if obj.order_items else "[]"
        return json.loads(items)

    def create(self, validated_data):
        shippingInfo = validated_data.pop("shipping")
        billingInfo = validated_data.pop("billing")

        order = self.Meta.model.objects.create(**validated_data)
        ShippingInfo.objects.create(order=order, **shippingInfo)

        return order

    def update(self, instance, validated_data):
        try:
            shipping = ShippingInfoSerializer(validated_data.pop("shipping")).data
            ShippingInfo.objects.update(**shipping)

            billing = BillingInfoSerializer(validated_data.pop("billing")).data
            BillingInfo.objects.update(**billing)
        finally:
            pass
        super().save(instance, validated_data)
        return instance