"""
Database menu module models.
"""

from decimal import Decimal
import os
import uuid

from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
)


class Menu(models.Model):
    """Database menu model."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)


def dish_image_file_path(instance, filename):
    """Generate file path for dish image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "dish", filename)


class Dish(models.Model):
    """Database dish model."""

    menu = models.ForeignKey(
        "menu.Menu", on_delete=models.CASCADE, related_name="dishes"
    )
    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    preparation_time = models.DurationField()
    is_vegetarian = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to=dish_image_file_path)
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
