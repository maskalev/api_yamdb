from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'
        return request.method in permissions.SAFE_METHODS
