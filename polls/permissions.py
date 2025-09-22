from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only allow owners of an object to edit it.
    Everyone else has read-only access.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions for GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.owner == request.user
