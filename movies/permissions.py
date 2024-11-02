from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to allow only superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the creator of a movie to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
