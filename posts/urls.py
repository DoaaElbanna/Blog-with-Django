from django.urls import path, include
from django.contrib import admin
from .views import (post_list, post_create, post_delete, post_detail, post_update)


# urls work from top to bottom, left to right
app_name = 'posts'
urlpatterns = [
    path('', post_list, name='list'),  # go to homepage
    path('create/', post_create, name='create'),
    path('<int:pk>/', post_detail, name='detail'),
    path('<int:pk>/edit/', post_update, name='update'),
    path('<int:pk>/delete/', post_delete, name='delete'),
]