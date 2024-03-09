from rest_framework import permissions


class BlockAnonymousUserMe(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action == 'me' and user.is_anonymous:
            return False
        return True
