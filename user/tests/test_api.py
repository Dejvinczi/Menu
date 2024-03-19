"""
User module API tests.
"""

import pytest
from django.urls import reverse
from rest_framework import status

REGISTER_USER_URL = reverse("user:register")
ME_URL = reverse("user:me")
TOKEN_PAIR_URL = reverse("user:token")
TOKEN_REFRESH_URL = reverse("user:token_refresh")


@pytest.mark.django_db
class TestPublicUserAPI:
    """Tests of public user API's"""

    def test_register_user_successful(self, client, django_user_model):
        """Test of creating a user in sucessful."""
        payload = {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "testuser1pass",
        }

        response = client.post(REGISTER_USER_URL, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.data
        assert "username" in response.data
        assert "email" in response.data
        assert response.data["username"] == payload["username"]
        assert response.data["email"] == payload["email"]

        user = django_user_model.objects.get(email=payload["email"])
        assert user.check_password(payload["password"])

    def test_register_user_email_unique_error(self, client, user_factory):
        """Test of creating user with email unique error."""
        payload = {
            "username": "anothertestuser1",
            "email": "testuser1@example.com",
            "password": "testuser1pass",
        }
        user_factory.create(email=payload["email"])
        response = client.post(REGISTER_USER_URL, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert len(response.data["email"]) == 1
        assert response.data["email"][0].code == "unique"

    def test_register_user_username_unique_error(self, client, user_factory):
        """Test of creating user with username unique error."""
        payload = {
            "username": "testuser1",
            "email": "anothertestuser1@example.com",
            "password": "testuser1pass",
        }
        user_factory.create(username=payload["username"])
        response = client.post(REGISTER_USER_URL, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
        assert len(response.data["username"]) == 1
        assert response.data["username"][0].code == "unique"

    def test_obtain_token_pair_successful(self, client, user_factory):
        """Test of obtaining token pair sucessful."""
        user_data = {
            "username": "testuser1",
            "email": "anothertestuser1@example.com",
            "password": "testuser1pass",
        }
        user_factory.create(**user_data)

        payload = {"email": user_data["email"], "password": user_data["password"]}
        response = client.post(TOKEN_PAIR_URL, data=payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_token_pair_empty_email_error(self, client, user_factory):
        """Test of obtaining token pair with empty email error."""
        user_data = {
            "username": "testuser1",
            "email": "anothertestuser1@example.com",
            "password": "testuser1pass",
        }
        user_factory.create(**user_data)

        payload = {"email": "", "password": user_data["password"]}
        response = client.post(TOKEN_PAIR_URL, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert len(response.data["email"]) == 1
        assert response.data["email"][0].code == "blank"

    def test_obtain_token_pair_empty_password_error(self, client, user_factory):
        """Test of obtaining token pair with empty email error."""
        user_data = {
            "username": "testuser1",
            "email": "anothertestuser1@example.com",
            "password": "testuser1pass",
        }
        user_factory.create(**user_data)

        payload = {"email": user_data["email"], "password": ""}
        response = client.post(TOKEN_PAIR_URL, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data
        assert len(response.data["password"]) == 1
        assert response.data["password"][0].code == "blank"

    def test_refresh_token_successful(self, client, user_factory):
        """Test of refreshing token successful."""
        user_data = {
            "username": "testuser1",
            "email": "anothertestuser1@example.com",
            "password": "testuser1pass",
        }
        user_factory.create(**user_data)

        payload = {"email": user_data["email"], "password": user_data["password"]}
        response = client.post(TOKEN_PAIR_URL, data=payload)

        payload2 = {"refresh": response.data["refresh"]}
        response2 = client.post(TOKEN_REFRESH_URL, data=payload2)

        assert response2.status_code == status.HTTP_200_OK
        assert "access" in response2.data

    def test_refresh_token_empty_refresh_token_error(self, client):
        """Test of refreshing token with empty refresh token error."""
        payload = {"refresh": ""}

        response = client.post(TOKEN_REFRESH_URL, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "refresh" in response.data
        assert len(response.data["refresh"]) == 1
        assert response.data["refresh"][0].code == "blank"

    def test_retrive_user_information_unauthorized_error(self, client):
        """Test of retriving user information with no logged user."""
        response = client.post(ME_URL, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateUserAPI:
    """Tests of private user API's"""

    def test_retrive_user_information_successful(self, api_client, user_factory):
        """Test of retriving user information about logged user."""
        user_data = {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "testuser1pass",
        }
        user = user_factory(**user_data)
        auth_client = api_client(user=user)

        response = auth_client.get(ME_URL)

        assert response.status_code == status.HTTP_200_OK
        assert "username" in response.data
        assert "email" in response.data
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email
