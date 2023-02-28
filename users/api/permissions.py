from rest_framework.permissions import BasePermission



class IsBuyerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_buyer)


class IsVendorUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_vendor)