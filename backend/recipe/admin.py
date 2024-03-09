from django.contrib import admin

from .models import Ingredient, MeasurimentUnit, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

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
class MeasurimentUnitAdmin(admin.ModelAdmin):

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
class IngredientAdmin(admin.ModelAdmin):

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


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = ['name', 'author']

    ordering = [
        'name',
    ]
    search_fields = ['name', 'author', 'tags']
    list_filter = ['name', 'author', 'tags']
