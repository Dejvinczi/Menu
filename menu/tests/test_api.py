"""
Menu module API tests.
"""

import pytest
from django.urls import reverse
from rest_framework import status

MENUS_URL = reverse("menu:menus-list")


def get_menu_detail_url(menu_id):
    """Create and return an menu detail URL."""
    return reverse("menu:menus-detail", args=[menu_id])


def get_menu_dish_list_url(menu_id):
    """Create and return an menu dishes list URL."""
    return reverse("menu:menu-dishes-list", kwargs={"menu_pk": menu_id})


def get_dish_detail_url(dish_id):
    """Create and return an dish detail URL."""
    return reverse("menu:dishes-detail", args=[dish_id])


@pytest.mark.django_db
class TestPublicMenuAPI:
    """Tests of public menu API's"""

    def test_cannot_create_menu(self, client):
        """Test of creating menu with unauthorized - error."""
        response = client.post(MENUS_URL, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_update_menu(self, client, menu_factory):
        """Test of updating menu with unauthorized - error."""
        menu = menu_factory()

        response = client.post(get_menu_detail_url(menu.id), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_delete_menu(self, client, menu_factory):
        """Test of deleting menu with unauthorized - error."""
        menu = menu_factory()

        response = client.delete(get_menu_detail_url(menu.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_list_empty_menus(self, client, menu_factory):
        """Test of retrieving empty menus."""
        menu_factory()

        response = client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_can_list_non_empty_menus(self, client, dish_factory):
        """Test of retrieving non empty menus."""
        dish = dish_factory()

        response = client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_data = response.data[0]
        assert dish.menu.id == response_menu_data["id"]

    def test_cannot_retrive_empty_menu(self, client, menu_factory):
        """Test of retrieving empty menu - error."""
        menu = menu_factory()

        response = client.get(get_menu_detail_url(menu.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_can_retrive_non_empty_menu(self, client, dish_factory):
        """Test of retrieving non-empty menu."""
        dish = dish_factory()

        response = client.get(get_menu_detail_url(dish.menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert dish.menu.id == response.data["id"]


@pytest.mark.django_db
class TestPrivateMenuAPI:
    """Tests of private menu API's"""

    def test_can_list_empty_menus(self, api_auth_client, menu_factory):
        "Test of listing empty menus."
        auth_client = api_auth_client()
        menu = menu_factory()
        print(menu.id)
        response = auth_client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_data = response.data[0]
        print(response_menu_data["id"])
        assert menu.id == response_menu_data["id"]

    @pytest.mark.skip("ToDo")
    def test_can_list_non_empty_menus(self, api_auth_client, dish_factory, menu_model):
        "Test of listing non empty menus."
        print(menu_model.objects.all())
        auth_client = api_auth_client()
        dish = dish_factory()
        print(menu_model.objects.all())
        response = auth_client.get(MENUS_URL)
        print(response.data)
        print(dish.menu.id)
        print(dish.menu.name)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_data = response.data[0]
        assert dish.menu.id == response_menu_data["id"]

    def test_can_create_menu(self, api_auth_client, menu_model):
        "Test of creating menu."
        auth_client = api_auth_client()
        payload = {"name": "TestMenu1", "description": "TestMenu1Desc"}
        response = auth_client.post(MENUS_URL, data=payload)

        assert response.status_code == status.HTTP_201_CREATED

        menus = menu_model.objects.all()
        assert len(menus) == 1

        menu = menus.first()
        assert menu.name == payload["name"]
        assert menu.description == payload["description"]

    def test_can_update_menu(self, api_auth_client, menu_factory):
        "Test of updating menu."
        auth_client = api_auth_client()
        menu = menu_factory()

        payload = {"name": "UpdatedMenuName1"}
        response = auth_client.patch(get_menu_detail_url(menu.id), data=payload)
        menu.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert menu.id == response.data["id"]
        assert menu.name == payload["name"]

    def test_can_delete_menu(self, api_auth_client, menu_factory, menu_model):
        "Test of deleting menu."
        auth_client = api_auth_client()
        menu = menu_factory()

        response = auth_client.delete(get_menu_detail_url(menu.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not menu_model.objects.filter(id=menu.id).first()


@pytest.mark.django_db
class TestPublicMenuDishAPI:
    """Tests of private menu dishes API's"""

    def test_cannot_create_menu_dish(self, client, menu_factory):
        """Test of creating menu dishes - error."""
        menu = menu_factory()

        response = client.post(get_menu_dish_list_url(menu.id), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_retrive_empty_menu_dishes(self, client, menu_factory):
        """Test of retrieving empty menu dishes - error."""
        menu = menu_factory()

        response = client.get(get_menu_dish_list_url(menu.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_can_retrive_non_empty_menu_dishes(self, client, dish_factory):
        """Test of retrieving non-empty menu dishes."""
        dish = dish_factory()

        response = client.get(get_menu_dish_list_url(dish.menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_dish_data = response.data[0]
        assert dish.id == response_menu_dish_data["id"]


@pytest.mark.django_db
class TestPrivateMenuDishAPI:
    """Tests of private menu dishes API's"""

    def test_can_create_menu_dish(self, api_auth_client, menu_factory):
        """Test of creating menu dishes."""
        auth_client = api_auth_client()
        menu = menu_factory()
        payload = {
            "name": "TestDishName1",
            "description": "TestDishDescription1",
            "price": "20.55",
            "preparation_time": "00:00:30",
            "is_vegetarian": True,
        }

        response = auth_client.post(get_menu_dish_list_url(menu.id), data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == payload["name"]
        assert response.data["description"] == payload["description"]
        assert response.data["price"] == payload["price"]
        assert response.data["preparation_time"] == payload["preparation_time"]
        assert response.data["is_vegetarian"] == payload["is_vegetarian"]

    def test_can_retrive_empty_menu_dishes(self, api_auth_client, menu_factory):
        """Test of retrieving empty menu dishes."""
        auth_client = api_auth_client()
        menu = menu_factory()

        response = auth_client.get(get_menu_dish_list_url(menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_can_retrive_non_empty_menu_dishes(self, client, dish_factory):
        """Test of retrieving non-empty menu dishes."""
        dish = dish_factory()

        response = client.get(get_menu_dish_list_url(dish.menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_dish_data = response.data[0]
        assert dish.id == response_menu_dish_data["id"]


@pytest.mark.django_db
class TestPublicDishAPI:
    """Tests of dish API's"""

    def test_cannot_retrieve_dish(self, client, dish_factory):
        """Test of retrieving dish - error."""
        dish = dish_factory()

        response = client.get(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_update_dish(self, client, dish_factory):
        """Test of updating dish - error"""
        dish = dish_factory()

        response = client.patch(get_dish_detail_url(dish.id), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_delete_dish(self, client, dish_factory):
        """Test of deleting dish - error"""
        dish = dish_factory()

        response = client.delete(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateDishAPI:
    """Tests of dish API's"""

    def test_can_retrieve_dish(self, api_auth_client, dish_factory):
        """Test of retrieving dish."""
        auth_client = api_auth_client()
        dish = dish_factory()

        response = auth_client.get(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == dish.id

    def test_can_update_dish(self, api_auth_client, dish_factory):
        """Test of updating dish"""
        auth_client = api_auth_client()
        dish = dish_factory()
        payload = {"name": "NewTestDishName1"}

        response = auth_client.patch(get_dish_detail_url(dish.id), data=payload)
        dish.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == dish.id
        assert dish.name == payload["name"]

    def test_can_delete_dish(self, api_auth_client, dish_factory):
        """Test of deleting dish"""
        auth_client = api_auth_client()
        dish = dish_factory()

        response = auth_client.delete(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
