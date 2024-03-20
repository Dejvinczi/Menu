"""
Menu module API views.
"""

from django.db.models import Count
from rest_framework import (
    viewsets,
    mixins,
    permissions,
)

from menu import models
from menu.api import serializers


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menu.objects.prefetch_related("dishes").all()
    serializer_class = serializers.MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.annotate(dishes_number=Count("dishes")).filter(
                dishes_number__gt=1
            )

        return self.queryset


class DishViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer
