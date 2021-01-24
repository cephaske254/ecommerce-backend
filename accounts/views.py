from django.shortcuts import render
from rest_framework import generics, views
from . import serializers

# Create your views here.


class Register(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class PasswordReset(views.APIView):
    pass

class PasswordResetConfirm(views.APIView):
    pass