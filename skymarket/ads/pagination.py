from rest_framework.pagination import PageNumberPagination


class AdPagination(PageNumberPagination):
    page_size = 4


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
