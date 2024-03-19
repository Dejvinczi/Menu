"""
Menu module model tests.
"""

import pytest
from datetime import timedelta

from ..models import Menu, Dish
from .factories import MenuFactory


@pytest.mark.django_db
class TestMenuModel:
    """Dish model tests."""

    def test_create_menu_successful(self):
        """Test creating new menu."""
        menu_data = {"name": "TestMenu1", "description": "TestMenuDescription1"}
        menu = Menu.objects.create(**menu_data)

        for k, v in menu_data.items():
            assert getattr(menu, k, None) == v

    def test_create_dish_successful(self):
        """Test creating new dish."""
        menu = MenuFactory.create()

        dish_data = {
            "menu": menu,
            "name": "TestDish1",
            "description": "TestDishDescription1",
            "price": 15.32,
            "preparation_time": timedelta(minutes=30),
            "is_vegetarian": True,
        }
        dish = Dish.objects.create(**dish_data)

        for k, v in dish_data.items():
            assert getattr(dish, k, None) == v
