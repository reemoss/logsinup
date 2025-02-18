from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow POST, PUT, DELETE only for admin users
        return request.user and request.user.is_superuser