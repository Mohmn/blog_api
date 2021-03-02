from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from rest_framework.parsers import JSONParser
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions

# SAFE_METHODS = ['GET', 'HEAD'] #rewrote it beacuse when i clicked on options user got permision to delete non-authored items


class PostUserWritePermission(BasePermission):


    def has_object_permission(self, request, view, obj):

        
        if request.method == "GET":
            print(obj.creator.id,request.user.id,request.method,obj)

            return True

        return obj.creator == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message="checking "
    # def has_permission(self,request)
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return False

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

class ListBlogs(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self, request, format="json"):
        """
        Return a list of all users.
        """
        # print(self.get_permissions())
        # print(self.check_permissions(request))
        # self.check_object_permissions(request, obj)
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request, format="json"):
        """
        create  a new blog
        """
        print(request.data)
        data = request.data
        # if isinstance(request.data, QueryDict):
        request.data._mutable = True
        data['creator'] = request.user.id
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(APIView):
    permission_classes = [IsAuthenticated,PostUserWritePermission]
    """
    Retrieve, update or delete a code snippet.
    """
    """
    # u have to explicitly call check_object_permissions(self.request, obj) 
    to check if the fucntion passes the perission checks 
    or in other words here if the user owes the object or not

    check out https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py
    it it implemented there

    i also overwrided get_object(self, pk) method here

    """
    
    def get_object(self, pk):
        try:
            obj = Blog.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """
        Return a list of all users.
        """
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Return a list of all users.
        """
        
        blog = self.get_object(pk)
        blog.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)