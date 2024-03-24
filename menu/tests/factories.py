"""
Menu module model factories.
"""

import factory

from menu import models


class MenuFactory(factory.django.DjangoModelFactory):
    """Menu model factory."""

    name = factory.Sequence(lambda n: f"Menu{n}")
    description = factory.Sequence(lambda n: f"Description{n}")

    class Meta:
        model = models.Menu


class DishFactory(factory.django.DjangoModelFactory):
    """Dish model factory."""

    menu = factory.SubFactory(MenuFactory)
    name = factory.Sequence(lambda n: f"Dish{n}")
    description = factory.Sequence(lambda n: f"Description{n}")
    price = factory.Faker("random_number", digits=2)
    preparation_time = factory.Faker("time_delta", end_datetime=None)
    is_vegetarian = factory.Faker("boolean")

    class Meta:
        model = models.Dish
