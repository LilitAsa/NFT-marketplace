from rest_framework.pagination import PageNumberPagination

class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)