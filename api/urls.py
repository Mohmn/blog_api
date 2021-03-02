from django.urls import path
from . import views

urlpatterns = [
    # path('blogs/', views.blog_list),
    # path('blogs/<int:pk>/', views.blog_detail),
    path('blogs/', views.ListBlogs.as_view()),
    path('blogs/<int:pk>/',views.BlogDetail.as_view())
]