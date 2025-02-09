from rest_framework import pagination

class StandardResultSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100


class SetPagination(pagination.PageNumberPagination):
    page_size = 15
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100