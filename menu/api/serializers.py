"""
Menu module API serializers.
"""

from rest_framework import serializers

from ..models import (
    Menu,
    Dish,
)


class DishSerializer(serializers.ModelSerializer):
    """Dish serializer."""

    class Meta:
        model = Dish
        fields = "__all__"
        read_only_fields = ("id", "added_on", "updated_on")


class MenuSerializer(serializers.ModelSerializer):
    """Menu serializer."""

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ("id", "added_on", "updated_on")
