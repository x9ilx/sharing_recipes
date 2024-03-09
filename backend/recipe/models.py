from django.db import models
from django.contrib.auth import get_user_model


user_model = get_user_model()


class Tag(models.Model):
    name = models.CharField('Наименование', max_length=200)
    color = models.CharField('Цветовой код (HEX)', max_length=7)
    slug = models.SlugField('Уникальный slug', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class MeasurimentUnit(models.Model):
    name = models.CharField('Наименование', max_length=200)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Наименование', max_length=200)
    measurement_unit = models.ForeignKey(
        MeasurimentUnit,
        verbose_name='Единица измерения',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Игредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Наименование', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField('Время приготовления (минуты)')
    image = models.ImageField(upload_to='recipe/images/')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги')
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиенты', through='RecipeIngredients'
    )
    author = models.ForeignKey(
        user_model, verbose_name='Автор', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='+',
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Игредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe-ingredient',
            )
        ]


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='+',
    )
    user = models.ForeignKey(
        user_model,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_list',
    )

    class Meta:
        verbose_name = 'Список покупок пользователей'
        verbose_name_plural = 'Списки покупок пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='recipe-user',
            )
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='+',
    )
    user = models.ForeignKey(
        user_model,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_list',
    )

    class Meta:
        verbose_name = 'Избранный рецепт пользователей'
        verbose_name_plural = 'Избранные рецепты пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='recipe-user',
            )
        ]
