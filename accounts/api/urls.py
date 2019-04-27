from django.urls import path, include
from django.contrib import admin
from .views import (
    UserCreateApiView,
    UserLoginApiView,

)


# urls work from top to bottom, left to right
app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('register/', UserCreateApiView.as_view(), name='register'),
]