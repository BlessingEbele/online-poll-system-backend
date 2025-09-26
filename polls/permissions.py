# polls/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyOrAuthenticated(BasePermission):
    """
    Allow unrestricted GET/HEAD/OPTIONS requests.
    Require authentication for POST/PUT/PATCH/DELETE.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
