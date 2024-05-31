from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResultsPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class ConditionalPagination(ResultsPagination):

    def paginate_queryset(self, queryset, request, view=None):
        # Check if pagination parameters are provided in the request
        page = request.query_params.get(self.page_query_param)
        page_size = request.query_params.get(self.page_size_query_param)

        if page or page_size:
            # If pagination parameters are present, use default pagination
            return super().paginate_queryset(queryset, request, view)
        else:
            # If no pagination parameters, return the entire queryset
            self.page = None
            self.page_size = None
            self.request = request
            self.display_page_controls = False
            return list(queryset)

    def get_paginated_response(self, data):
        if self.page is not None:
            # If paginated, return standard paginated response
            return super().get_paginated_response(data)
        else:
            # If not paginated, include pagination metadata with the full queryset
            return Response({
                'count': len(data),
                'next': None,
                'previous': None,
                'results': data
            })
