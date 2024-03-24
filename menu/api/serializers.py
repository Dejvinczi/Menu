"""
Menu module API serializers.
"""

from rest_framework import serializers

from ..models import (
    Menu,
    Dish,
)


class DishSerializer(serializers.ModelSerializer):
    """Serializer for dish."""

    class Meta:
        model = Dish
        exclude = ("menu",)
        read_only_fields = ("id", "added_on", "updated_on", "image")


class DishImageSerializer(serializers.ModelSerializer):
    """Serializer for dish image uploading."""

    image = serializers.ImageField()

    class Meta:
        model = Dish
        fields = ("id", "image")
        read_only_fields = ("id",)
        extra_kwargs = {"image": {"write_only": True}}


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu."""

    class Meta:
        model = Menu
        fields = ("id", "name", "description", "added_on", "updated_on")
        read_only_fields = ("id", "added_on", "updated_on")


class MenuDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for menu."""

    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ("id", "added_on", "updated_on")
