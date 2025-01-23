from django.db.models import Q

from dental_app.utils.response import BaseResponse

class SearchMixin:
    """
    Mixin to add search functionality to APIs.
    """
    search_fields = []

    def apply_search(self, queryset, search_query):
        if search_query:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(query)
        return queryset
    

class PaginationMixin:
    """
    Mixin to add pagination functionality to APIs.
    """
    def paginate_and_serialize(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return BaseResponse(
            data=serializer.data,
            status=200)