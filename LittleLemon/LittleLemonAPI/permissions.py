from rest_framework.permissions import BasePermission, SAFE_METHODS

class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if request.user.groups.filter(name="Managers").exists():
            return request.method in ["GET", "DELETE", "PATCH"]
        if request.user.groups.filter(name="Delivery Crew").exists():
            return request.method in ["GET", "PATCH"]
        return request.method in ["GET", "POST", "PATCH"]
  
class MenuItemPermission(BasePermission):
    def has_permission(self, request, view):
        # print(request.user.groups.all())
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.groups.filter(name="Managers").exists():
            return request.method in ["POST", "PUT", "PATCH", "DELETE"]
        return False

class CartPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.groups.filter(name="Managers").exists():
            return False
        if request.user.groups.filter(name="Delivery Crew").exists():
            return False
        return request.method in ["GET", "POST", "DELETE"]

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Managers").exists()

class IsDelivery(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Delivery Crew").exists()