from rest_framework import permissions


class ManageOwnObjects(permissions.BasePermission):
    """Allow user to manage their own objects"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own object"""
        return obj.owner == request.user


class CantManageRootFolder(permissions.BasePermission):
    """Deny user to manage their own root folder"""

    def has_object_permission(self, request, view, obj):
        """Check user is not trying to edit their own root folder"""
        return obj != request.user.root_folder
