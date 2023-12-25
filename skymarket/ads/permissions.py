# здесь производится настройка пермишенов для нашего проекта
from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    message = 'you are not the owner or administrator of this post'

    def has_object_permission(self, request, view, obj) -> bool:
        if obj.author == request.user:
            return True
        return request.user.is_staff
