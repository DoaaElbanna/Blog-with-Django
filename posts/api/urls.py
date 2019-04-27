from django.urls import path, include
from django.contrib import admin
from .views import (
    PostDetailApiView,
    PostDeleteApiView,
    PostListApiView,
    PostUpdateApiView,
    PostCreateApiView
    )


# urls work from top to bottom, left to right
app_name = 'posts'
urlpatterns = [
    path('', PostListApiView.as_view(), name='list'),  # go to homepage
    path('create/', PostCreateApiView.as_view(), name='create'),
    path('<int:pk>/', PostDetailApiView.as_view(), name='detail'),
    path('<int:pk>/edit/', PostUpdateApiView.as_view(), name='update'),
    path('<int:pk>/delete/', PostDeleteApiView.as_view(), name='delete'),
]