from rest_framework.permissions import BasePermission

class BlogUserWritePermission(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method == "GET":
            return True

        return obj.creator == request.user

class AuthorUserWritePermission(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method == "GET":
            return True

        return obj == request.user