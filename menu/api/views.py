"""
Menu module API views.
"""

from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import (
    viewsets,
    mixins,
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from menu import models
from menu.api import serializers


class MenuViewSet(viewsets.ModelViewSet):
    """API view set for menu."""

    queryset = models.Menu.objects.prefetch_related("dishes").all()
    serializer_class = serializers.MenuDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        match self.action:
            case "list" | "create":
                return serializers.MenuSerializer
            case _:
                return self.serializer_class

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.annotate(dishes_number=Count("dishes")).filter(
                dishes_number__gte=1
            )

        return self.queryset


class MenuDishViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """API view set for menu dishes."""

    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        menu = get_object_or_404(models.Menu, pk=self.kwargs["menu_pk"])

        if not self.request.user.is_authenticated:
            return get_list_or_404(
                self.queryset.annotate(menu__dishes_number=Count("menu__dishes")),
                menu__dishes_number__gte=1,
                menu=menu,
            )

        return self.queryset

    def perform_create(self, serializer):
        menu_pk = self.kwargs["menu_pk"]
        return serializer.save(menu_id=menu_pk)


class DishViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        match self.action:
            case "upload_image":
                return serializers.DishImageSerializer
            case _:
                return self.serializer_class

    @action(
        detail=True,
        methods=["POST"],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Upload an image to dish."""
        dish = self.get_object()
        serializer = self.get_serializer(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
