from rest_framework.permissions import BasePermission

from django.utils import timezone


class IsWorkHours(BasePermission):
    def has_permission(self, request, view):
        current_hour = timezone.localtime().hour
        print("=" * 70)
        print("=" * 70)
        print(current_hour)
        print("=" * 70)
        print("=" * 70)

        return 9 <= current_hour < 12
