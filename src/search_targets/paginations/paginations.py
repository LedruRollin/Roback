
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class PaginationWithTotalCount(PageNumberPagination):
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            'total-count': self.page.paginator.count,
            'data': data,
        })
