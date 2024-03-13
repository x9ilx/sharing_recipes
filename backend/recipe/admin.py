from core.admin_mixins import ModelAdminElementsWidthMixIn
from django.contrib import admin
from django.utils.safestring import mark_safe

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
        'name',
        'text',
        'cooking_time',
        'show_image',
        'image',
        'tags',
        'author',
    ]
    readonly_fields = ['show_image']
    list_display = ['name', 'author']

    ordering = [
        'name',
    ]
    search_fields = ['name', 'author', 'tags']
    list_filter = [
        ('author', admin.RelatedOnlyFieldListFilter),
        ('tags', admin.RelatedOnlyFieldListFilter),
    ]
    inlines = [
        RecipeIngredientsInline,
    ]

    def show_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            )
        )

    show_image.short_description = 'Текущее изображение'


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(ModelAdminElementsWidthMixIn):

    list_display = ['recipe', 'ingredient', 'amount']

    ordering = [
        'recipe',
        'ingredient',
    ]
    search_fields = ['recipe__name', 'ingredient__name']
    list_filter = [('ingredient', admin.RelatedOnlyFieldListFilter)]
