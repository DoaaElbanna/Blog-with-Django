from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner to this object"
    # my_safe_methods = ["PUT", "GET"]
    #
    # def has_permission(self, request, view):  # check on the view level
    #     if request.method in self.my_safe_methods:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):  # The instance level

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


