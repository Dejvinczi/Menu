"""

"""

from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allows logged-in users access to all operations,
    but read-only access for non-logged-in users.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        return request.method in permissions.SAFE_METHODS
