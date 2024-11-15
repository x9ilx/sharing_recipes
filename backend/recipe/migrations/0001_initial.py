# Generated by Django 3.2.3 on 2024-03-09 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='Наименование'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Игредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='MeasurimentUnit',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='Наименование'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='Наименование'
                    ),
                ),
                ('text', models.TextField(verbose_name='Описание')),
                (
                    'cooking_time',
                    models.PositiveIntegerField(
                        verbose_name='Время приготовления (минуты)'
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        upload_to='recipe/images/',
                        verbose_name='Файл с изображением',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Автор',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='Наименование'
                    ),
                ),
                (
                    'color',
                    models.CharField(
                        max_length=7, verbose_name='Цветовой код (HEX)'
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        max_length=200,
                        unique=True,
                        verbose_name='Уникальный slug',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.PositiveIntegerField(verbose_name='Количество'),
                ),
                (
                    'ingredient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to='recipe.ingredient',
                        verbose_name='Ингредиент',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipe_ingredients',
                        to='recipe.recipe',
                        verbose_name='Рецепт',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ингредиенты в рецепте',
                'verbose_name_plural': 'Игредиенты в рецептах',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                through='recipe.RecipeIngredients',
                to='recipe.Ingredient',
                verbose_name='Ингредиенты',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipe.Tag', verbose_name='Тэги'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='recipe.measurimentunit',
                verbose_name='Единица измерения',
            ),
        ),
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(
                fields=('recipe', 'ingredient'), name='recipe-ingredient'
            ),
        ),
    ]
