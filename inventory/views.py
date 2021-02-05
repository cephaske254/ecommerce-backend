from django.shortcuts import render, get_object_or_404
from rest_framework import generics, response, status, views, permissions
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
import datetime
from django.core.mail import send_mail
import threading


class TopProducts(generics.ListAPIView):
    serializer_class = serializers.ProductListMini

    def get_queryset(self):
        queryset = models.Product.objects
        if self.request.user.is_authenticated and self.request.user.has_perms:
            return queryset.all()
        return queryset.filter(available=True).order_by("?")[:20]


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

        product = get_object_or_404(
            models.Product, slug=self.request.data.get("product", {}).get("slug")
        )

        if not fileImage and image is not None:
            serializer.save(
                product=product,
                image=buildImage(image, "banner_%s" % self.request.data.get("title")),
            )
        else:
            serializer.save(product=product, image=fileImage)

    def get_queryset(self):
        queryset = models.BannerAd.objects

        if self.request.user.is_authenticated and self.request.user.has_perms:
            return queryset.all()
        return queryset.filter(active=True)


class BannerAdsDetail(generics.RetrieveUpdateDestroyAPIView, BannerAdListCreate):
    lookup_field = "product__slug"
    lookup_url_kwarg = "slug"

    def get(self, request, slug, *args, **kwargs):
        banner_ad = self.get_queryset().filter(product__slug=slug).first()

        product = get_object_or_404(models.Product, slug=slug)

        serialize = serializers.ProductListMini(product)
        serialize.context["request"] = request
        data = {
            **self.get_serializer(banner_ad).data,
            "vacant": False if banner_ad else True,
        }

        return response.Response(data=data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        banner = self.queryset.filter(
            product__slug=self.request.data.get("product", {}).get("slug")
        )

        if banner:
            return super().update(request, *args, **kwargs)

        return super().create(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        image = self.request.data.get("image", None)
        fileImage = self.request.FILES.get("image", None)

        if not fileImage and image is not None:
            serializer.save(
                image=buildImage(image, "banner_%s" % self.request.data.get("title")),
            )
        else:
            serializer.save()


class visitorIn(views.APIView):
    permission_classes = [permissions.AllowAny]

    def mail(self):
        date = datetime.datetime.now().strftime("%B %d, %Y %H:%M")
        send_mail(
            "NEW VISITOR",
            "A NEW VISITOR ACCESSED YOUR PAGE on %s" % date,
            from_email="developers@uxinfiniti.com",
            recipient_list=["cephaske254@gmail.com"],
        )

    def post(self, request):
        thread = threading.Thread(target=self.mail)
        thread.run()

        return response.Response(data={})
