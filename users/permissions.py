from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_staff or
                    request.user.role == request.user.UserRole.ADMIN)
        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_staff or request.user.UserRole.ADMIN)


class IsStaffOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return(
                obj.author == request.user or
                request.method in permissions.SAFE_METHODS or
                request.user.role == request.user.UserRole.MODERATOR or
                request.user.role == request.user.UserRole.ADMIN
            )
