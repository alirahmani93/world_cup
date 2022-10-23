import math
from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class BasePaginator(LimitOffsetPagination):
    ordering = ['-created_time']


class CustomPageNumberPagination(BasePaginator):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('total_page', math.ceil(self.count / self.limit)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class ResponsePaginator(CustomPageNumberPagination):
    page_size = 15
    max_page_size = 30
