from django_filters.rest_framework import filters, FilterSet

from recipe.models import Ingredient


class NameParamSearchFilter(FilterSet):
    name = filters.CharFilter(method='filter_name')

    class Meta:
        model = Ingredient
        fields = ['name']

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__istartswith=value).order_by('name')
