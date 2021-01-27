from django.shortcuts import render
from rest_framework import generics, response, status
from . import serializers
from . import models
from .utils import (
    setProductCategories,
    saveProductImages,
    removeProductImages,
    addProductBrand,
    buildImage,
)
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
        data["brand"] = addProductBrand(brand_data)

        product = serializer.save(**data)

        addProductBrand(brand_data)
        setProductCategories(self.request, product)
        saveProductImages(self.request, product)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductListCreate
    queryset = models.Product.objects.all()
    lookup_field = "slug"

    def perform_update(self, serializer):
        brand_data = self.request.data.get("brand")
        data = {}
        data["brand"] = addProductBrand(brand_data)

        product = serializer.save(**data)

        saveProductImages(self.request, product)
        setProductCategories(self.request, product)
        removeProductImages(self.request)

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


class BannerAdListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.BannerAdSerializer

    def perform_create(self, serializer):
        image = self.request.data.get("image", None)
        fileImage = self.request.FILES.get("image", None)

        if not fileImage and image is not None:
            serializer.validated_data["image"] = buildImage(
                image, "banner_%s" % self.request.get("title")
            )
        else:
            serializer.save(image=fileImage)

    def get_queryset(self):
        queryset = models.BannerAd.objects

        if self.request.user.is_authenticated and self.request.user.has_perms:
            return queryset.all()
        return queryset.filter(active=True)


class BannerAdsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.BannerAdSerializer
    queryset = models.BannerAd.objects.all()