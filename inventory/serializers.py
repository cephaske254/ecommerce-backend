from rest_framework import serializers
from . import models
import json


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Brand


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class CategorySerializerMini(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = ["name"]


class ProductListMini(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    # price = serializers.CharField(read_only=True)

    class Meta:
        model = models.Product
        fields = (
            "id",
            "slug",
            "name",
            "price",
            "market_price",
            "discount_price",
            "image",
            "image_count",
        )

        extra_kwargs = {"price": {"read_only": True}}

    def get_image(self, obj):
        host = self.context.get("request")
        image = obj.image
        host_name = host.get_host()

        is_secure = "https://" if host.is_secure() else "http://"

        if image:
            return is_secure + host_name + image
        return None


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListMini(read_only=True, many=True)

    class Meta:
        model = models.Category
        fields = ("id", "name", "products")


class ProductListCreate(serializers.ModelSerializer):
    colors = serializers.JSONField(required=False)
    images = ImageSerializer(required=False, read_only=True, many=True)
    categories = serializers.SerializerMethodField()
    brand = BrandSerializer(read_only=True)
    slug = serializers.ReadOnlyField()

    class Meta:
        model = models.Product
        fields = (
            "id",
            "slug",
            "name",
            "categories",
            "description",
            "brand",
            "colors",
            "price",
            "market_price",
            "discount_price",
            "available",
            "images",
        )
        extra_kwargs = {"price": {"read_only": True}}

    def get_categories(self, obj):
        objects = obj.categories.all()
        data = [(category.name) for category in objects]
        return data

        # return data

    def update(self, validated_data, *args, **kwargs):
        return super().update(validated_data, *args, **kwargs)
