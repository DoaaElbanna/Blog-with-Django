from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.filters import (
     SearchFilter,
     OrderingFilter,
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    )


from rest_framework.permissions import (
     AllowAny,  # allow unrestricted access
     IsAuthenticated,  # deny permission to any unauthenticated user, and allow permission otherwise
     IsAdminUser,  # deny permission to any user, unless user.is_staff is True
     IsAuthenticatedOrReadOnly  # allow authenticated users to perform any request
)
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
)

User = get_user_model()


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserLoginApiView(APIView):  # Base Api view
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)  # rest api response not the django response
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


