import django_filters as filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class NameParamSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__pk', lookup_expr='exact')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='slug',
        method='filter_tag'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    def filter_tag(self, queryset, name, value):
        if len(value) == 0:
            return queryset.distinct()
        return queryset.filter(tags__in=value).order_by('-pub_date').distinct()
