from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

class IsTenant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'tenant'

class IsLeaseOperator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'lease_operator'

class IsBroker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'broker'

class IsSocietyManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'society_manager'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_staff)

class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('owner', 'admin')
