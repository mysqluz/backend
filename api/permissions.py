from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if view.action == 'retrieve':
            return True
        if not request.user.is_authenticated:
            return False
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        return False


class UserUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        return obj == request.user or request.user.is_admin


class CategoryProblemNewsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and request.user.is_admin
        return True
