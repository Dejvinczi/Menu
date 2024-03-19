"""
Menu model API url's.
"""

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from .views import (
    MenuViewSet,
    DishViewSet,
)

d_router = DefaultRouter()
d_router.register("menus", MenuViewSet)
d_router.register("dishes", DishViewSet)

app_name = "menu"

urlpatterns = [
    path("", include(d_router.urls)),
]
