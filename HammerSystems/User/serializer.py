from rest_framework import serializers
from .models import User

class CodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
