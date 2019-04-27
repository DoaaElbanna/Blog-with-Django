from django.db.models import Q
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
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly
from comments.models import Comment

from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
    )


# use class based view, use Generic views


class CommentCreateApiView(CreateAPIView):  # Return a single model instance
    queryset = Comment.objects.all()
    # serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)  # none is the default value if not there parent id
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )

    # def perform_create(self, serializer):  # to let any user do this action not only the default
    #     serializer.save(user=self.request.user)


# class CommentDetailApiView(RetrieveAPIView):  # Return a single model instance
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetailSerializer


class CommentDetailApiView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):  # Update
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):  # To update
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):  # To delete
        return self.destroy(request, *args, **kwargs)

# class PostDeleteApiView(DestroyAPIView):  # Delete a single model instance
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer


# class PostUpdateApiView(RetrieveUpdateAPIView):  # Update or read a single model instance
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)


class CommentListApiView(ListAPIView):  # Return collection of model instances
    # queryset = Post.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ["content", "user__first_name"]
    pagination_class = PostPageNumberPagination  # it will work only for the parent comments

    def get_queryset(self, *args, **kwargs):  # override
        # queryset_list = super(PostListApiView, self.get_queryset(*args, **kwargs))
        queryset_list = Comment.objects.filter(id__gte=0)  # filter(user=self.request.user)
        query = self.request.GET.get("query")
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list
