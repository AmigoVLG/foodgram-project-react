from rest_framework.permissions import SAFE_METHODS, BasePermission


class PermissionDenied(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        author = obj.author
        if request.method in SAFE_METHODS:
            return True
        if user.is_staff:
            return True
        return author == user
