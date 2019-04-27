from django.urls import path, include
from django.contrib import admin
from .views import (
    CommentCreateApiView,
    CommentDetailApiView,
    CommentListApiView,

)


# urls work from top to bottom, left to right
app_name = 'comments'
urlpatterns = [
    path('', CommentListApiView.as_view(), name='list'),
    path('create/', CommentCreateApiView.as_view(), name='create'),
    path('<int:pk>', CommentDetailApiView.as_view(), name='thread'),
    # path('<int:pk>/delete/', comment_delete, name='delete'),
]