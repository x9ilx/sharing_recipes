from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        'recipe.Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_list',
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
                name='shopping-list-recipe-user',
            )
        ]
        ordering = ['-recipe__pub_date']

    def __str__(self):
        return f'Список покупок: {self.recipe.name}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        'recipe.Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    user = models.ForeignKey(
        user_model,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранный рецепт пользователей'
        verbose_name_plural = 'Избранные рецепты пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='favorite-recipe-user',
            )
        ]
        ordering = ['-recipe__pub_date']

    def __str__(self):
        return f'Избранное: {self.recipe.name}'


class Subscribe(models.Model):
    author = models.ForeignKey(
        user_model,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='+',
    )
    user = models.ForeignKey(
        user_model,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscribes',
    )

    class Meta:
        verbose_name = 'Подписки пользователей'
        verbose_name_plural = 'Подписки пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='author-user',
            )
        ]
        ordering = ['author__username']

    def __str__(self):
        return f'Подписка {self.user.username} на {self.author.username}'
