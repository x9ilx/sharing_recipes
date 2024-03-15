from io import BytesIO

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import AuthorOrReadOnly, OnlyAuth
from user.docs.shopping_cart_dpf import ShoppingCartDocGeneratePDF
from user.serializers import RecipeGetMiniSerializer, ShoppingCatrSerializer

from .filters import RecipeFilter
from .models import Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    TagSerializer,
)

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
    http_method_names = ['get', 'post', 'patch', 'delete']
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

        if not current_user.is_anonymous:
            if is_in_shopping_cart == '1':
                queryset = Recipe.objects.filter(
                    shopping_list__user=current_user
                )

            if is_favorited == '1':
                queryset = Recipe.objects.filter(favorites__user=current_user)

        return queryset.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def create_or_update_recipe(self, create, request, kwargs):
        current_user = self.request.user
        data = request.data
        data['author'] = current_user.pk
        res_status = status.HTTP_201_CREATED if create else status.HTTP_200_OK

        if create:
            serializer = RecipeCreateSerializer(data=request.data)
        else:
            recipe = get_object_or_404(Recipe, pk=kwargs['pk'])

            if current_user != recipe.author:
                return Response(
                    {'detail': 'Только автор может изменять рецепт'},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = RecipeCreateSerializer(
                recipe, data=data, partial=False
            )

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance_serializer = RecipeGetSerializer(
            instance, context={'request': self.request}
        )
        return Response(instance_serializer.data, res_status)

    def create(self, request, *args, **kwargs):
        return self.create_or_update_recipe(
            create=True, request=request, kwargs=kwargs
        )

    def update(self, request, *args, **kwargs):
        return self.create_or_update_recipe(
            create=False, request=request, kwargs=kwargs
        )

    def add_to_shopping_cart(self, current_user, recipe):
        if current_user.shopping_list.filter(recipe=recipe).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен в список покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {}
        data['user'] = current_user.pk
        data['recipe'] = recipe.pk

        serializer = ShoppingCatrSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        result = RecipeGetMiniSerializer(
            instance=recipe, context={'request': self.request}
        )
        return Response(result.data, status=status.HTTP_201_CREATED)

    def delete_from_shopping_cart(self, current_user, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if current_user.shopping_list.filter(recipe=recipe).exists():
            current_user.shopping_list.filter(recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Рецепт не добавлен в список покупок'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=['DELETE', 'POST'],
        url_path='shopping_cart',
        url_name='user-shopping-cart',
        permission_classes=[OnlyAuth],
    )
    def user_delete_create_shoping_cart(self, request, pk=-1):
        current_user = request.user

        if request.method == 'POST':
            if not Recipe.objects.filter(pk=pk).exists():
                return Response(
                    {'errors': 'Рецепт не существует'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = Recipe.objects.get(pk=pk)
            return self.add_to_shopping_cart(current_user, recipe)

        if request.method == 'DELETE':
            return self.delete_from_shopping_cart(current_user, pk)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        url_name='download-shopping-cart',
        permission_classes=[OnlyAuth],
    )
    def user_download_shopping_cart(self, request, pk=-1):
        current_user = request.user

        pdf_template = ShoppingCartDocGeneratePDF(
            current_user=current_user,
            buffer=BytesIO(),
        )
        response = HttpResponse(content_type='application/pdf')
        pdf = pdf_template.get_pdf()
        response.write(pdf)
        return response
