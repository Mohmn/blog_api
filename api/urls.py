from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.ListBlogs.as_view()),
    path('blogs/<int:pk>/',views.BlogDetail.as_view()),
    path('register/',views.createUser.as_view()),
    path('user/<int:pk>/',views.updateUsers.as_view()),
]