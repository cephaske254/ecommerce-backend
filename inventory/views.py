from django.shortcuts import render
from rest_framework import generics, response, status
from . import serializers
from . import models
from .utils import setCategories, saveImages, removeImages, addBrand
from rest_framework import filters


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.ProductListCreate
    queryset = models.Product.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = serializers.ProductListMini
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        category_data = self.request.data.get("categories")
        brand_data = self.request.data.get("brand")
        data = {}
        data["brand"] = addBrand(brand_data)

        product = serializer.save(**data)

        addBrand(brand_data)
        setCategories(self.request, product)
        saveImages(self.request, product)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductListCreate
    queryset = models.Product.objects.all()
    lookup_field = "slug"

    def perform_update(self, serializer):
        brand_data = self.request.data.get("brand")
        data = {}
        data["brand"] = addBrand(brand_data)

        product = serializer.save(**data)

        saveImages(self.request, product)
        setCategories(self.request, product)
        removeImages(self.request)

    def _allowed_methods(self):
        return [
            m
            for m in super(ProductDetail, self)._allowed_methods()
            if m not in ["PATCH", "DELETE", "HEAD", "OPTIONS", "PUT"]
        ]


class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CategoryDetailSerializer
    queryset = models.Category.objects.all()
    lookup_field = "slug"

    def put(self, request, *args, **kwargs):
        self.serializer_class = serializers.CategorySerializer
        return super().put(request, *args, **kwargs)
