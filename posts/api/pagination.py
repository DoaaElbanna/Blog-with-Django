from rest_framework.pagination import(
     LimitOffsetPagination,
     PageNumberPagination  # accepts a single number page number in the request query parameters.

)


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class PostPageNumberPagination(PageNumberPagination):
    page_size = 2