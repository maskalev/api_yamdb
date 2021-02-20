from rest_framework import permissions


class SiteAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_autenticated:
            return request.user.is_admin
        return False
