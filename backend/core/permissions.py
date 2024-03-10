from rest_framework import permissions


class OnlyAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        return True
