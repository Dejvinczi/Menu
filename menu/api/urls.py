"""
Menu model API url's.
"""

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from menu.api import views

# menus
menu_router = DefaultRouter()
menu_router.register(r"menus", views.MenuViewSet)
menu_router.register(r"dishes", views.DishViewSet)

# menu dishes
dishes_router = routers.NestedSimpleRouter(menu_router, r"menus", lookup="menu")
dishes_router.register(r"dishes", views.MenuDishViewSet, basename="id")

app_name = "menu"

urlpatterns = [
    path("", include(menu_router.urls), name="menus"),
    path("", include(dishes_router.urls), name="dishes"),
]
