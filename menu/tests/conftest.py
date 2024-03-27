"""
Configuration our tests user module tests.
"""

import pytest

from io import BytesIO
from PIL import Image
from dataclasses import dataclass

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from menu.models import Menu, Dish
from menu.tests.factories import MenuFactory, DishFactory


@pytest.fixture
def menu_factory():
    """Fixture to provide MenuFactory."""
    return MenuFactory


@pytest.fixture
def dish_factory():
    """Fixture to provide DishFactory."""
    return DishFactory


@pytest.fixture
def menu_model():
    """Fixture to provide Menu model"""
    return Menu


@pytest.fixture
def dish_model():
    """Fixture to provide Dish model"""
    return Dish


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


@dataclass
class TestImageFile:
    name: str
    content: str
    file: SimpleUploadedFile


@pytest.fixture
def test_image_file():
    """Fixture to provide TestImageFile dataclass with image."""
    f = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(f, "png")
    f.seek(0)

    file_name = "test_image.jpg"
    file_content = f.read()

    file = SimpleUploadedFile(
        name=file_name,
        content=file_content,
        content_type="image/jpeg",
    )

    yield TestImageFile(file_name, file_content, file)

    file.close()


@pytest.fixture
def email_backend_setup(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
