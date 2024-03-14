"""
Configuration our tests user module tests.
"""

import pytest
from factories import UserFactory

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_factory_model():
    """Fixture to provide User Factory."""
    return UserFactory


@pytest.fixture
def api_client():
    """Fixture to provide authorized client if you specify the user."""

    def create_client(user=None):
        client = APIClient()

        if user is None:
            user = get_user_model().objects.create_user(
                username="testuser",
                email="testuser@example.com",
                password="testpassword123",
            )

        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

        return client

    return create_client
