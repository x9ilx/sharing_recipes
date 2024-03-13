from core.admin_mixins import ModelAdminElementsWidthMixIn
from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Favorite, ShoppingList, Subscribe

user_model = get_user_model()


apps.get_app_config('auth').verbose_name = 'Пользователи и авторизация'
admin.site.unregister(user_model)

admin.site.site_header = 'Foodgram Admin'
admin.site.site_title = 'Foodgram Admin Portal'
admin.site.index_title = 'Welcome to Foodgram'


@admin.register(user_model)
class UserAdmin(admin.ModelAdmin):

    list_display = [
        'username',
        'email',
    ]
    ordering = [
        'username',
    ]
    search_fields = [
        'username',
        'email',
    ]
    list_filter = [
        'username',
        'email',
    ]

    class Meta:
        app_label = 'My APP name'


@admin.register(ShoppingList)
class ShoppingListAdmin(ModelAdminElementsWidthMixIn):

    list_display = ['recipe', 'user']

    ordering = [
        'user',
        'recipe',
    ]
    search_fields = ['recipe', 'user__username']
    list_filter = [('user', admin.RelatedOnlyFieldListFilter)]


@admin.register(Favorite)
class FavoriteListAdmin(ModelAdminElementsWidthMixIn):

    list_display = ['recipe', 'user']

    ordering = [
        'user',
        'recipe',
    ]
    search_fields = ['recipe__name', 'user__username']
    list_filter = [('user', admin.RelatedOnlyFieldListFilter)]


@admin.register(Subscribe)
class SubscribeAdmin(ModelAdminElementsWidthMixIn):

    list_display = ['author', 'user']

    ordering = [
        'author',
        'user',
    ]
    search_fields = ['author__username', 'user__username']
    list_filter = [
        ('author', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
    ]
