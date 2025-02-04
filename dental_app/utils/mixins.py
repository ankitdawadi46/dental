from django.db.models import Q

from dental_app.utils.pagination import CustomPagination
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
    Mixin to provide paginated or non-paginated responses.
    """

    pagination_class = CustomPagination  # Ensure this is defined in your project

    def list(self, request, *args, **kwargs):
        """
        Returns either paginated or unpaginated data based on the `paginated` query param.
        """
        paginated = request.GET.get("paginated", "true").lower() == "true"
        queryset = self.filter_queryset(self.get_queryset())

        if paginated:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=serializer.data)
