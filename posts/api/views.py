from django.db.models import Q
from rest_framework.filters import (
     SearchFilter,
     OrderingFilter,
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    )

from rest_framework.pagination import(
     LimitOffsetPagination,
     PageNumberPagination  # accepts a single number page number in the request query parameters.

)

from rest_framework.permissions import (
     AllowAny,  # allow unrestricted access
     IsAuthenticated,  # deny permission to any unauthenticated user, and allow permission otherwise
     IsAdminUser,  # deny permission to any user, unless user.is_staff is True
     IsAuthenticatedOrReadOnly  # allow authenticated users to perform any request
)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from posts.models import Post
from .serializers import (
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    )


# use class based view, use Generic views


class PostCreateApiView(CreateAPIView):  # Return a single model instance
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):  # to let any user do this action not only the default
        serializer.save(user=self.request.user)


class PostDetailApiView(RetrieveAPIView):  # Return a single model instance
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    # lookup_field = "slug"


class PostDeleteApiView(DestroyAPIView):  # Delete a single model instance
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostUpdateApiView(RetrieveUpdateAPIView):  # Update or read a single model instance
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostListApiView(ListAPIView):  # Return collection of model instances
    # queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ["title", "content", "user__first_name"]
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):  # override
        # queryset_list = super(PostListApiView, self.get_queryset(*args, **kwargs))
        queryset_list = Post.objects.all()  # filter(user=self.request.user)
        query = self.request.GET.get("query")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list





