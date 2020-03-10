from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserModel


class UserSer(ModelSerializer):
    class Meta:
        model = UserModel,
        fields = '__all__'
