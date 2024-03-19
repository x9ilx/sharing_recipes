from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from recipe import constants


user_model = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LENGTH_NAME_FIELD
    )
    color = models.CharField(
        'Цветовой код (HEX)',
        max_length=constants.MAX_LENGTH_COLOR_FIELD
    )
    slug = models.SlugField(
        'Уникальный slug',
        unique=True,
        max_length=constants.MAX_LENGTH_SLUG_FIELD
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class MeasurimentUnit(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LENGTH_NAME_FIELD
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LENGTH_NAME_FIELD
    )
    measurement_unit = models.ForeignKey(
        MeasurimentUnit,
        verbose_name='Единица измерения',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Игредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=constants.MAX_LENGTH_NAME_FIELD
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (минуты)',
        validators=[
            validators.MinValueValidator(
                limit_value=constants.MIN_INTEGER_FIELD
            ),
            validators.MaxValueValidator(
                limit_value=constants.MAX_INTEGER_FIELD
            ),
        ]
    )
    image = models.ImageField(
        upload_to='recipe/images/', verbose_name='Файл с изображением'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тэги')
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиенты', through='RecipeIngredients'
    )
    author = models.ForeignKey(
        user_model,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='+',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            validators.MinValueValidator(
                limit_value=constants.MIN_INTEGER_FIELD
            ),
            validators.MaxValueValidator(
                limit_value=constants.MAX_INTEGER_FIELD
            ),
        ]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Игредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe-ingredient',
            )
        ]
        ordering = ['recipe__pub_date']

    def __str__(self) -> str:
        return f'{self.recipe}: {self.ingredient}'
