import django_filters as filters
from django.db.models import Q
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class NameParamSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__pk', lookup_expr='exact')
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug', method='filter_tag'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    def filter_tag(self, queryset, name, value):
        query = Q()
        for tag in value:
            if Tag.objects.filter(slug=tag).exists():
                query |= Q(tags__slug=tag)

        return queryset.filter(query)
