"""
Menu module API views.
"""

from django.db.models import Count
from rest_framework import viewsets

from ..models import (
    Menu,
    Dish,
)
from .permission import IsAuthenticatedOrReadOnly
from .serializers import (
    MenuSerializer,
    DishSerializer,
)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.prefetch_related("dishes").all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.annotate(dishes_number=Count("dishes")).filter(
                count_dishes__gt=1
            )

        return self.queryset


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
