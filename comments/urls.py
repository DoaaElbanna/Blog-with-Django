from django.urls import path, include
from django.contrib import admin
from .views import (comment_thread, comment_delete)


# urls work from top to bottom, left to right
app_name = 'comments'
urlpatterns = [
    path('<int:pk>/', comment_thread, name='thread'),
    path('<int:pk>/delete/', comment_delete, name='delete'),
]