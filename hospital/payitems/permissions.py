from rest_framework import permissions
from django.contrib.auth.models import Permission


class IsPyitemsOrReadOnly(permissions.BasePermission):
    """
        自定义权限，只读或有Pyitems的所有权限可以访问
    """

    def has_permission(self, request, view):
        # 只读method
        if request.method in permissions.SAFE_METHODS:
            return True

        # pyitems的所有权限
        permission_list = []
        for i in Permission.objects.filter(content_type_id=11):
            permission_list.append('database.' + i.codename)
        permission_pyitems = tuple(permission_list)

        return request.user.has_perms(permission_pyitems)


class IsRegisterItemsOrReadOnly(permissions.BasePermission):
    """
        自定义权限，只读或有RegisterItems的所有权限可以访问
    """

    def has_permission(self, request, view):
        # 只读method
        if request.method in permissions.SAFE_METHODS:
            return True

        # RegisterItems的所有权限
        permission_list = []
        for i in Permission.objects.filter(content_type_id=12):
            permission_list.append('database.' + i.codename)
        permission_pyitems = tuple(permission_list)

        return request.user.has_perms(permission_pyitems)
