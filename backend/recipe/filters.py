from django_filters.rest_framework import filters, FilterSet

from recipe.models import Ingredient


class NameParamSearchFilter(FilterSet):
    name = filters.CharFilter(method='filter_name')

    class Meta:
        model = Ingredient
        fields = ['name']

    def filter_name(self, queryset, name, value):
        queryset_is_start_with = Ingredient.objects.filter(
            name__istartswith=value
        ).order_by('name')
        queryset_icontains = Ingredient.objects.filter(
            name__icontains=value
        ).order_by('name')
        return queryset_is_start_with.union(queryset_icontains, all=True)
