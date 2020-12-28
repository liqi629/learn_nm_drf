from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationManual(PageNumberPagination):
    page_query_param = 'p'  # 设置显示第几页的key
    #默认情况下每页显示的条数
    page_size = 4
    page_size_query_param = 's'  # 设置每页显示的key
    max_page_size = 50 # 指定前端分页最大条数