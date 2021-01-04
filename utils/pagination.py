# from rest_framework.pagination import PageNumberPagination

from django.conf import settings
from rest_framework import pagination


class PageNumberPaginationManual(pagination.PageNumberPagination):


    # Client can control the page using this query parameter.
    page_query_param = 'page'
    page_query_description = '第几页'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'size'
    page_size_query_description = '每页几条'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 50

    def get_paginated_response(self, data):
        response = super(PageNumberPaginationManual,self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current_pag_num'] = self.page.number
        return response
