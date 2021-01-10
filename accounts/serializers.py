from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = (
            "firstName",
            "lastName",
            "phone",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}
        model = User

    def validate(self, data):
        password = data.get("password")
        password2 = data.pop("password2")
        if password != password2:
            raise serializers.ValidationError({"password2": "Passwords didnt match!"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user