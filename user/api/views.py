"""
User module API views.
"""

from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import (
    UserSerializer,
)


class CreateUserAPIView(generics.CreateAPIView):
    """Create new user API view."""

    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []


class MeAPIView(generics.RetrieveAPIView):
    """Manage user API view."""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Retrive and return the authenticated user."""
        return self.request.user
