from django.shortcuts import render
from rest_framework import generics, response, views
from . import serializers

# Create your views here.
class OrderAPIView(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer


class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = serializer_class.Meta.model.objects.all()


class OrderStats(views.APIView):
    permission_classes = ()

    def get(self, request):
        return response.Response(
            data={
                "general": [20, 299, 123,20,65,55,107,27,143,345,167,104,56],
                "returning": [12, 23,41,56,35,13,51,61,5,22,27,12],
            }
        )
