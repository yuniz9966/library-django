from rest_framework.permissions import BasePermission

class CanGetStatisticPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_get_statistic')
