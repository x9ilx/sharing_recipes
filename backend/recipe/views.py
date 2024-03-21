from io import BytesIO

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import AuthorOrReadOnly, OnlyAuthor
from user.docs.shopping_cart_dpf import ShoppingCartDocGeneratePDF
from user.serializers import (
    FavoriteSerializer,
    RecipeGetMiniSerializer,
    ShoppingCatrSerializer,
)
from .filters import NameParamSearchFilter
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
    filterset_class = NameParamSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = RecipeGetSerializer
    permission_classes = [
        AuthorOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Recipe.objects.all()

        current_user = self.request.user
        is_in_shopping_cart = self.request.GET.get('is_in_shopping_cart', '0')
        is_favorited = self.request.GET.get('is_favorited', '0')
        author = self.request.GET.get('author', None)
        tags = self.request.GET.getlist('tags', None)

        if not current_user.is_anonymous:
            if is_in_shopping_cart == '1':
                queryset = Recipe.objects.filter(
                    shopping_list__user=current_user
                )

            if is_favorited == '1':
                queryset = Recipe.objects.filter(favorites__user=current_user)

        if tags:
            queryset = queryset.filter(tags__slug__in=tags)

        if author:
            queryset = queryset.filter(author_id=author)

        return queryset.select_related('author').prefetch_related(
            'tags', 'ingredients'
        ).distinct().order_by('-pub_date')

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

    def add_to_shopping_cart_or_favorites(
        self, current_user, recipe_id, table
    ):
        recipe = Recipe.objects.filter(pk=recipe_id).first()

        if not recipe:
            return Response(
                {'errors': 'Объект не существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        field = getattr(current_user, table)

        serializer_class = (
            ShoppingCatrSerializer
            if table == 'shopping_list'
            else FavoriteSerializer
        )

        if field.filter(recipe=recipe).exists():
            return Response(
                {'errors': 'Объект уже добавлен в список'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {}
        data['user'] = current_user.pk
        data['recipe'] = recipe.pk

        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = RecipeGetMiniSerializer(
            instance=recipe, context={'request': self.request}
        )
        return Response(result.data, status=status.HTTP_201_CREATED)

    def delete_from_shopping_cart_or_favorites(
        self, current_user, recipe_id, table
    ):
        field = getattr(current_user, table)
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        deleted_object = field.filter(recipe=recipe)

        if deleted_object.exists():
            deleted_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Объект не добавлен в список'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=['DELETE', 'POST'],
        url_path='shopping_cart',
        url_name='user-shopping-cart',
        permission_classes=[OnlyAuthor],
    )
    def user_delete_create_shoping_cart(self, request, pk):
        current_user = request.user

        if request.method == 'POST':
            return self.add_to_shopping_cart_or_favorites(
                current_user, pk, 'shopping_list'
            )

        if request.method == 'DELETE':
            return self.delete_from_shopping_cart_or_favorites(
                current_user, pk, 'shopping_list'
            )

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        url_name='download-shopping-cart',
        permission_classes=[OnlyAuthor],
    )
    def user_download_shopping_cart(self, request):
        current_user = request.user

        pdf_template = ShoppingCartDocGeneratePDF(
            current_user=current_user,
            buffer=BytesIO(),
        )
        response = HttpResponse(content_type='application/pdf')
        pdf = pdf_template.get_pdf()
        response.write(pdf)
        return response

    @action(
        detail=True,
        methods=['DELETE', 'POST'],
        url_path='favorite',
        url_name='user-favorite',
        permission_classes=[OnlyAuthor],
    )
    def user_delete_create_favorite(self, request, pk):
        current_user = request.user

        if request.method == 'POST':
            return self.add_to_shopping_cart_or_favorites(
                current_user, pk, 'favorites'
            )

        if request.method == 'DELETE':
            return self.delete_from_shopping_cart_or_favorites(
                current_user, pk, 'favorites'
            )
