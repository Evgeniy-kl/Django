from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'USER':
            return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'ADMIN':
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'MODERATOR':
            return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
