"""
User module API serializers.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    def create(self, val_data):
        """Create new user in system and return user instance."""
        user = get_user_model().objects.create_user(**val_data)

        return user

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
