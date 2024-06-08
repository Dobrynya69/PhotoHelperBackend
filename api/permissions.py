from rest_framework import permissions


class IsAuthorSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True


    def has_object_permission(self, request, view, object):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if object.user == request.user:
            return True

        return False