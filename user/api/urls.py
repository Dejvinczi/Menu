"""
User module API urls.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CreateUserAPIView,
    MeAPIView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="register"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
