from rest_framework.pagination import CursorPagination

class CursorSetPagination(CursorPagination):
    cursor_query_param = 'blogs'
    page_size = 2
    page_size_query_param = 'page_size'
    ordering = 'created_at' # '-created' is default

# def list(self, request, *args, **kwargs):
#     queryset = self.filter_queryset(self.get_queryset())

#     page = self.paginate_queryset(queryset)
#     if page is not None:
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)

#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)