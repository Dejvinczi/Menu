"""
User module models tests.
"""

import pytest

from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUser:
    """User model tests."""

    def test_create_user_with_email_successful(self):
        user_data = {
            "email": "testuser@example.com",
            "password": "testuser123",
        }
        user = get_user_model().objects.create_user(**user_data)

        assert user.email == user_data["email"]
        assert user.check_password(user_data["password"])

    def test_create_user_without_email_error(self):
        user_data = {
            "email": "",
            "password": "testuser123",
        }
        with pytest.raises(ValueError) as e_info:
            get_user_model().objects.create_user(**user_data)

        assert str(e_info.value) == "User must have an email address."

    def test_create_superuser_with_email_successful(self):
        user_data = {
            "email": "testsuperuser@example.com",
            "password": "testsuperuser123",
        }
        user = get_user_model().objects.create_superuser(**user_data)

        assert user.email == user_data["email"]
        assert user.check_password(user_data["password"])

    def test_create_superuser_without_email_error(self):
        user_data = {
            "email": "",
            "password": "testsuperuser123",
        }
        with pytest.raises(ValueError) as e_info:
            get_user_model().objects.create_superuser(**user_data)

        assert str(e_info.value) == "User must have an email address."
