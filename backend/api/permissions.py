
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class PermissionDenied(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        author = obj.author
        if request.method in SAFE_METHODS:
            return True
        return author == user


