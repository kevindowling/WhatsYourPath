# permissions.py
from rest_framework import permissions

class IsSpecificUser(permissions.BasePermission):

    def has_permission(self, request, view):
        specific_user_name = "assistant" #[TODO] Make sure that users must have unique names
        return request.user.name == specific_user_name
