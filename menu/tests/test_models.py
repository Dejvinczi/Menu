"""
Menu module model tests.
"""

import pytest
from datetime import timedelta

from menu.models import Menu, Dish


@pytest.mark.django_db
class TestMenuModel:
    """Dish model tests."""

    def test_create_menu_successful(self):
        """Test creating new menu."""
        menu_data = {"name": "TestMenu1", "description": "TestMenuDescription1"}
        menu = Menu.objects.create(**menu_data)

        assert menu.name == menu_data["name"]
        assert menu.description == menu_data["description"]

    def test_create_dish_successful(self, menu_factory):
        """Test creating new dish."""
        menu = menu_factory()
        dish_data = {
            "menu": menu,
            "name": "TestDish1",
            "description": "TestDishDescription1",
            "price": 15.32,
            "preparation_time": timedelta(minutes=30),
            "is_vegetarian": True,
        }

        dish = Dish.objects.create(**dish_data)

        assert dish.menu == dish_data["menu"]
        assert dish.name == dish_data["name"]
        assert dish.description == dish_data["description"]
        assert dish.price == dish_data["price"]
        assert dish.preparation_time == dish_data["preparation_time"]
        assert dish.is_vegetarian == dish_data["is_vegetarian"]

    def test_create_dish_with_image_successful(self, menu_factory, test_image_file):
        """Test creating new dish."""
        menu = menu_factory()

        dish_data = {
            "menu": menu,
            "name": "TestDish1",
            "description": "TestDishDescription1",
            "price": 15.32,
            "preparation_time": timedelta(minutes=30),
            "is_vegetarian": True,
            "image": test_image_file.file,
        }

        dish = Dish.objects.create(**dish_data)

        assert dish.menu == dish_data["menu"]
        assert dish.name == dish_data["name"]
        assert dish.description == dish_data["description"]
        assert dish.price == dish_data["price"]
        assert dish.preparation_time == dish_data["preparation_time"]
        assert dish.is_vegetarian == dish_data["is_vegetarian"]
        assert dish.image.read() == test_image_file.content
        dish.image.delete()
