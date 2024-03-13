"""
User application models tests.
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
