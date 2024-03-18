import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipe.models import (
    Ingredient,
    MeasurimentUnit,
    Recipe,
    RecipeIngredients,
    Tag,
)
from user.serializers import UserSerializer

user_model = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurimentUnit
        fields = [
            'id',
            'name',
        ]


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='ingredient', read_only=True)
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredients
        fields = [
            'id',
            'name',
            'amount',
            'measurement_unit',
        ]


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipe_ingredients', many=True
    )
    author = UserSerializer()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def check_favorites_or_shopping_list(self, table, obj):
        current_user = self.context['request'].user

        if current_user.is_anonymous:
            return False

        field = getattr(current_user, table)

        return field.filter(recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.check_favorites_or_shopping_list('favorites', obj)

    def get_is_in_shopping_cart(self, obj):
        return self.check_favorites_or_shopping_list('shopping_list', obj)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'text',
            'cooking_time',
            'image',
            'tags',
            'ingredients',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        ]

        extra_kwargs = {field: {'read_only': True} for field in fields}


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=True
    )
    image = Base64ImageField()
    ingredients = serializers.ListField(required=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = [
            'name',
            'text',
            'cooking_time',
            'image',
            'tags',
            'ingredients',
            'author',
        ]
        extra_kwargs = {field: {'required': True} for field in fields}

    def validate_ingredients(self, value):
        if not isinstance(value, list) or not len(value) > 0:
            raise serializers.ValidationError('Обязательное поле')

        existing_ingredients = []
        for ingredient in value:
            amount = ingredient.get('amount', 0)

            if amount == 0:
                raise serializers.ValidationError(
                    'Необходимо указать количество ингредиентов'
                )

            if 'id' not in ingredient:
                raise serializers.ValidationError(
                    'Необходимо указать id ингредиента'
                )

            ingredient_id = ingredient.get('id', 0)
            ingredient_exists = Ingredient.objects.filter(
                pk=ingredient_id
            ).exists()

            if not ingredient_exists:
                raise serializers.ValidationError(
                    f'Ингредиента {ingredient_id} не существует'
                )

            if ingredient_id in existing_ingredients:
                raise serializers.ValidationError(
                    f'Ингредиент {ingredient_id} уже добавлен в список'
                )

            existing_ingredients.append(ingredient_id)

        return value

    def validate_tags(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                'Необходимо указать хотя бы один тег'
            )

        equal_tags = len(set(value)) != len(value)
        if equal_tags:
            raise serializers.ValidationError(
                'Нельзя указывать одинаковые теги'
            )

        return value

    def recipe_add_tag(self, recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)

    def recipe_add_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            recipe_ingredients = RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            recipe.recipe_ingredients.add(recipe_ingredients)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        self.recipe_add_tag(recipe, tags)
        self.recipe_add_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        instance = super().update(
            instance=instance, validated_data=validated_data
        )
        instance.recipe_ingredients.all().delete()
        instance.tags.through.objects.all().delete()

        self.recipe_add_tag(instance, tags)
        self.recipe_add_ingredients(instance, ingredients)

        return instance
