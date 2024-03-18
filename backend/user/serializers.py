from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipe.models import Recipe
from user.models import Favorite, ShoppingList, Subscribe

user_model = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=user_model.objects.all())],
    )

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {field: {'required': True} for field in fields}


class UserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user

        if current_user.is_anonymous:
            return False

        subscribe = current_user.subscribes.filter(author=obj).exists()
        return subscribe


class RecipeGetMiniSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'cooking_time',
            'image',
        ]


class SubscriptionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = [
            'author',
            'user',
        ]


class SubscriptionsGetSerializer(serializers.Serializer):
    author = UserSerializer(required=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    def get_recipe_limit_context(self):
        try:
            recipe_limit = int(self.context.get('recipes_limit', -1))
        except Exception:
            recipe_limit = -1

        return recipe_limit

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_recipes(self, obj):
        recipe_limit = self.get_recipe_limit_context()
        recipes = Recipe.objects.filter(author=obj.author)

        if recipe_limit > 0:
            recipes = recipes[:recipe_limit]

        return RecipeGetMiniSerializer(
            recipes, many=True, context=self.context
        ).data

    class Meta:
        fields = [
            'author',
            'recipes_count',
            'recipes',
            'user',
        ]


class ShoppingCatrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = [
            'recipe',
            'user',
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
            'recipe',
            'user',
        ]
