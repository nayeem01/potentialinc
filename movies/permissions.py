from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to allow only superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the creator of a movie to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow edit and delete if the user is the creator
        return obj.created_by == request.user
