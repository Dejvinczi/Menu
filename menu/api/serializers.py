"""
Menu module API serializers.
"""

from rest_framework import serializers

from app.helpers.serializers import DateTimeWithTimeZone
from menu import models


class DishSerializer(serializers.ModelSerializer):
    """Serializer for dish."""

    added_on = DateTimeWithTimeZone(read_only=True)
    updated_on = DateTimeWithTimeZone(read_only=True)

    class Meta:
        model = models.Dish
        exclude = ("menu",)
        read_only_fields = ("id", "image")


class DishImageSerializer(serializers.ModelSerializer):
    """Serializer for dish image uploading."""

    image = serializers.ImageField()

    class Meta:
        model = models.Dish
        fields = ("id", "image")
        read_only_fields = ("id",)
        extra_kwargs = {"image": {"write_only": True}}


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu."""

    added_on = DateTimeWithTimeZone(read_only=True)
    updated_on = DateTimeWithTimeZone(read_only=True)

    class Meta:
        model = models.Menu
        fields = ("id", "name", "description", "added_on", "updated_on")
        read_only_fields = ("id",)


class MenuDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for menu."""

    added_on = DateTimeWithTimeZone(read_only=True)
    updated_on = DateTimeWithTimeZone(read_only=True)
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = models.Menu
        fields = "__all__"
        read_only_fields = ("id",)
