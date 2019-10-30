from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    # has_permission is general level of permission.
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    # has_object_permission would be permission of accessing a specific object.
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff