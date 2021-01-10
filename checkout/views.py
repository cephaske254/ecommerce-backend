from django.shortcuts import render
from rest_framework import generics
from . import serializers

# Create your views here.
class OrderAPIView(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer


class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = serializer_class.Meta.model.objects.all()