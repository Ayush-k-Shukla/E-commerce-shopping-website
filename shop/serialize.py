from .models import Cart
from rest_framework import serializers

class cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
