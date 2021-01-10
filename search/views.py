from rest_framework import generics, views, response
from inventory import models as inventoryModels
from django.db.models import Q
import json
from django.core import serializers

# Create your views here.
class searchProducts(views.APIView):
    def get(self, request, *args, **kwargs):
        data = []
        query = request.GET.get("q", "")
        available = request.GET.get("available", False)

        queryset = inventoryModels.Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(categories__name__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(brand_id__name__icontains=query),
            available=available,
        ).all()
        return response.Response(data=queryset)


class searchCategories(views.APIView):
    def get(self, request, *args, **kwargs):
        data = []
        query = request.GET.get("q", "")
        available = request.GET.get("available", False)

        queryset = inventoryModels.Category.objects.filter(name__icontains=query).all()[
            :10
        ]
        return response.Response(data=queryset)


"""
available, brand, brand_id, categories, colors, deal, description, id, images, initial_price, name, slug
"""
