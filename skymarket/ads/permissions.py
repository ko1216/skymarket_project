# здесь производится настройка пермишенов для нашего проекта
from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    message = 'you are not the owner or administrator of this post'

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.author == request.user or request.user.is_staff


class IsCommentOwnerOrAdmin(BasePermission):
    message = 'You are not the owner or administrator of this comment'

    def has_permission(self, request, view):
        com_pk = int(view.kwargs.get('com_pk', 0))
        obj = view.get_object()

        if obj.id != com_pk:
            return False

        if hasattr(obj, 'ad'):
            return obj.author == request.user or request.user.is_staff

        return False
