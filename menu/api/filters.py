"""
Menu module fitlers
"""

from django_filters import rest_framework as filters

from menu import models


class MenuFilter(filters.FilterSet):
    """A filter to enable filter menus."""

    added_on_from = filters.DateTimeFilter(
        field_name="added_on",
        lookup_expr="gte",
    )
    added_on_to = filters.DateTimeFilter(
        field_name="added_on",
        lookup_expr="lte",
    )
    updated_on_from = filters.DateTimeFilter(
        field_name="updated_on",
        lookup_expr="gte",
    )
    updated_on_to = filters.DateTimeFilter(
        field_name="updated_on",
        lookup_expr="lte",
    )
    order_by = filters.OrderingFilter(
        fields=("name", "added_on", "updated_on", "dishes_num"),
    )

    class Meta:
        model = models.Menu
        fields = ("name",)


class DishFilter(filters.FilterSet):
    """A filter to enable filter dishes."""

    added_on_from = filters.DateTimeFilter(
        field_name="added_on",
        lookup_expr="gte",
    )
    added_on_to = filters.DateTimeFilter(
        field_name="added_on",
        lookup_expr="lte",
    )
    updated_on_from = filters.DateTimeFilter(
        field_name="updated_on",
        lookup_expr="gte",
    )
    updated_on_to = filters.DateTimeFilter(
        field_name="updated_on",
        lookup_expr="lte",
    )
    order_by = filters.OrderingFilter(fields=("name", "added_on", "updated_on"))

    class Meta:
        model = models.Dish
        fields = ("name",)
