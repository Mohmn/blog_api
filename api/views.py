from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from rest_framework.parsers import JSONParser
from .models import Blog,Author
from .serializers import BlogSerializer,AuthorSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from .permissions import BlogUserWritePermission,AuthorUserWritePermission



class ListBlogs(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [IsAuthenticated]

    
    def get(self, request, format="json"):
        """
        Return a list of all blogs.
        """
   
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request, format="json"):
        """
        create  a new blog
        """
#       beacause here req is of type queydict obj 
        data = request.data.dict()
        request.data._mutable = True 
        data['creator'] = request.user.id
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(APIView):
    permission_classes = [IsAuthenticated,BlogUserWritePermission]
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

class createUser(APIView):

    def post(self,request,format="json"):
        
        data = request.data.dict()
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateUsers(APIView):
    permission_classes = [IsAuthenticated,AuthorUserWritePermission]

    def get_object(self, pk):
        try:
            obj = Author.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,pk):

        user = self.get_object(pk)
        serializer = AuthorSerializer(user)
        return Response(serializer.data)

    def put(self,request,pk):
        user = self.get_object(pk)
        print(request.data)
        serializer = AuthorSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



