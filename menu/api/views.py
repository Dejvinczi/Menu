"""
Menu module API views.
"""

from django.db.models import Count
from rest_framework import (
    viewsets,
    permissions,
)

from menu import models
from menu.api import serializers


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menu.objects.prefetch_related("dishes").all()
    serializer_class = serializers.MenuDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        match self.action:
            case "list":
                return serializers.MenuSerializer
            case _:
                return self.serializer_class

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.annotate(dishes_number=Count("dishes")).filter(
                dishes_number__gte=1
            )

        return self.queryset


class DishViewSet(viewsets.ModelViewSet):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer

    def get_queryset(self):
        menu_pk = self.kwargs["menu_pk"]
        return self.queryset.filter(menu=menu_pk)

    def perform_create(self, serializer):
        menu_pk = self.kwargs["menu_pk"]
        return serializer.save(menu_id=menu_pk)
