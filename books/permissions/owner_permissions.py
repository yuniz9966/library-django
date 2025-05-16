from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBookOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.publisher


class IsStaffAndOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS \
            or request.user == obj.owner
