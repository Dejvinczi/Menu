"""
Configuration our tests user module tests.
"""

import pytest
from factories import UserFactory

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_factory():
    """Fixture to provide User Factory."""
    return UserFactory


@pytest.fixture
def api_client():
    """Fixture to provide API api_client."""
    return APIClient()


@pytest.fixture
def api_auth_client():
    """
    Fixture to provide authorized API api_client with possible specific user or default.
    """

    def create_api_auth_client(user=None):
        api_client = APIClient()

        if user is None:
            user = get_user_model().objects.create_user(
                username="testuser",
                email="testuser@example.com",
                password="testpassword123",
            )

        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

        return api_client

    return create_api_auth_client
