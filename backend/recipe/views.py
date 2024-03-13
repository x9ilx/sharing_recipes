from core.permissions import AuthorOrReadOnly
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Ingredient, Recipe, Tag
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, TagSerializer)

user_model = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all().select_related('measurement_unit')
    pagination_class = None

    filterset_fields = [
        'name',
    ]
    ordering = [
        'name',
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = [
        'name',
    ]
    search_fields = [
        'name',
    ]


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'del']
    serializer_class = RecipeGetSerializer
    permission_classes = [
        AuthorOrReadOnly,
    ]
    filterset_fields = [
        'author',
        'tags__slug',
    ]
    filterset_class = RecipeFilter

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(
                self.request, queryset, view=self
            )
        return queryset

    def get_queryset(self):
        queryset = Recipe.objects.all()
        current_user = self.request.user
        is_in_shopping_cart = self.request.GET.get('is_in_shopping_cart', '0')
        is_favorited = self.request.GET.get('is_favorited', '0')

        if is_in_shopping_cart == '1':
            queryset = Recipe.objects.filter(shopping_list__user=current_user)

        if is_favorited == '1':
            queryset = Recipe.objects.filter(favorites__user=current_user)

        return queryset.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        current_user = self.request.user
        data = request.data
        data['author'] = current_user.pk
        serializer = RecipeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance_serializer = RecipeGetSerializer(
            instance, context={'request': self.request}
        )
        return Response(
            instance_serializer.data, status=status.HTTP_201_CREATED
        )
