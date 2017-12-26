from django.db.models import CharField
from rest_framework import serializers
from .models import myUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myUser
        fields = ('username', 'password')
