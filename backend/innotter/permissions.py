from rest_framework.permissions import BasePermission
from user.models import User


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.Roles.USER:
            return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.Roles.ADMIN:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.Roles.MODERATOR:
            return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
