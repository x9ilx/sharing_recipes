from django.contrib import admin
from django.utils.safestring import mark_safe

from core.string_helpers import ru_plural
from core.admin_mixins import ModelAdminElementsWidthMixIn
from .models import Ingredient, MeasurimentUnit, Recipe, RecipeIngredients, Tag


@admin.register(Tag)
class TagAdmin(ModelAdminElementsWidthMixIn):

    list_display = [
        'name',
        'slug',
    ]

    ordering = [
        'name',
    ]
    search_fields = [
        'name',
        'slug',
    ]
    list_filter = [
        'slug',
        'name',
    ]


@admin.register(MeasurimentUnit)
class MeasurimentUnitAdmin(ModelAdminElementsWidthMixIn):

    list_display = [
        'name',
    ]

    ordering = [
        'name',
    ]
    search_fields = [
        'name',
    ]
    list_filter = [
        'name',
    ]


@admin.register(Ingredient)
class IngredientAdmin(ModelAdminElementsWidthMixIn):

    list_display = ['name', 'measurement_unit']

    ordering = [
        'name',
    ]
    search_fields = [
        'name',
    ]
    list_filter = [
        'name',
    ]


class RecipeIngredientsInline(admin.TabularInline):
    verbose_name = 'Игредиенты'
    verbose_name_plural = 'Ингредиенты'
    model = RecipeIngredients
    extra = 0
    max_num = 5
    classes = ['collapse ', 'extrapretty']
    fields = [
        'ingredient',
        'amount',
    ]


@admin.register(Recipe)
class RecipeAdmin(ModelAdminElementsWidthMixIn):

    fields = [
        'pub_date',
        'name',
        'text',
        'cooking_time',
        'show_image',
        'image',
        'tags',
        'author',
    ]
    readonly_fields = ['show_image', 'pub_date']
    list_display = ['name', 'author', 'favorites_count', 'pub_date']

    ordering = [
        '-pub_date',
        'name',
    ]
    search_fields = ['name', 'author__username', 'tags__name', 'tags__slug']
    list_filter = [
        ('author', admin.RelatedOnlyFieldListFilter),
        ('tags', admin.RelatedOnlyFieldListFilter),
    ]
    inlines = [
        RecipeIngredientsInline,
    ]

    def show_image(self, obj):
        return mark_safe(
            (
                f'<img src="{obj.image.url}" width="{obj.image.width}"'
                f'height={obj.image.height} />'
            )
        )

    show_image.short_description = 'Текущее изображение'

    def favorites_count(self, obj):
        favorites_count = obj.favorites.all().count()
        return mark_safe(
            f'{favorites_count} {ru_plural(favorites_count, "раз,раза,раз")}'
        )

    favorites_count.short_description = 'Количество добавления в избранное'


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(ModelAdminElementsWidthMixIn):

    list_display = ['recipe', 'ingredient', 'amount']

    ordering = [
        'recipe',
        'ingredient',
    ]
    search_fields = ['recipe__name', 'ingredient__name']
    list_filter = [('ingredient', admin.RelatedOnlyFieldListFilter)]
